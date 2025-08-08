from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from .models import User, Interest
from django.db import transaction
from .forms import SignUpForm, LoginForm, ProfileUpdateForm, TestForm
import json


def auth_view(request):
    """Страница авторизации/регистрации"""
    if request.user.is_authenticated:
        next_url = request.GET.get('next')
        return redirect(next_url or 'profile')
    
    login_form = LoginForm()
    signup_form = SignUpForm()
    
    if request.method == 'POST':
        if 'login' in request.POST:
            # Обработка входа
            login_form = LoginForm(request, data=request.POST)
            if login_form.is_valid():
                identifier = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                remember = login_form.cleaned_data.get('remember_me')
                # Пробуем также trim пробелы
                user = authenticate(request, username=(identifier or '').strip(), password=(password or ''))
                if user is not None:
                    login(request, user)
                    if remember:
                        # 2 недели
                        request.session.set_expiry(60 * 60 * 24 * 14)
                    else:
                        # До закрытия браузера
                        request.session.set_expiry(0)
                    return redirect(request.GET.get('next') or 'profile')
                else:
                    login_form.add_error(None, 'Неверные учетные данные')
        
        elif 'signup' in request.POST:
            # Обработка регистрации
            signup_form = SignUpForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save()
                # Принудительно аутентифицируем пользователя
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                return redirect('profile')
    
    context = {
        'login_form': login_form,
        'signup_form': signup_form,
    }
    return render(request, 'main/auth.html', context)


@login_required
def profile_view(request):
    """Личный кабинет пользователя"""
    user = User.objects.prefetch_related('interests').get(pk=request.user.pk)
    
    # Инициализируем формы по умолчанию
    form = ProfileUpdateForm(instance=user)
    test_form = TestForm(instance=user)
    
    # Отладка - выводим текущие значения пользователя
    print(f"Текущие значения пользователя: q1={user.question1}, q2={user.question2}, q3={user.question3}, q4={user.question4}, q5={user.question5}")
    print(f"Общий балл: {user.test_score}")
    
    if request.method == 'POST':
        if 'update_interests' in request.POST:
            # Обновление интересов
            form = ProfileUpdateForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect('profile')
        
        elif 'update_test' in request.POST:
            # Обновление теста
            test_form = TestForm(request.POST, instance=user)
            if test_form.is_valid():
                test_form.save()
                user.calculate_test_score()
                user.save()
                return redirect('profile')
            else:
                pass  # Тихо обрабатываем ошибки формы
    
    context = {
        'user': user,
        'form': form,
        'test_form': test_form,
        'test_score': user.test_score,
    }
    return render(request, 'main/profile.html', context)


@login_required
def search_view(request):
    """Страница поиска собеседника"""
    user = request.user
    
    # Проверяем, есть ли у пользователя интересы
    if not user.interests.exists():
        return redirect('profile')
    
    context = {
        'user': user,
    }
    return render(request, 'main/search.html', context)


@login_required
@require_http_methods(["POST"])
def find_match(request):
    """AJAX запрос для поиска собеседника"""
    user = request.user
    
    # Помечаем пользователя как ищущего
    user.is_searching = True
    user.save()
    
    # Ищем подходящего собеседника с блокировкой для избежания гонок
    match = None
    with transaction.atomic():
        # Обновляем пользователя из БД и ищем совпадение
        user.refresh_from_db()
        match = user.find_match()
    
    if match:
        # Убираем обоих из поиска
        user.is_searching = False
        user.save()
        match.is_searching = False
        match.save()
        
        return JsonResponse({
            'status': 'success',
            'user_id': match.id,
            'match_username': match.username,
            'match_interests': list(match.interests.values_list('name', flat=True)),
            'match_social_url': match.social_url,
        })
    
    # Оставляем пользователя в поиске, если не нашли совпадение
    return JsonResponse({
        'status': 'no_match',
        'message': 'Подходящий собеседник не найден. Попробуйте позже!'
    })











@login_required
def logout_view(request):
    """Выход из системы"""
    logout(request)
    return redirect('auth')


@login_required
def user_profile_view(request, user_id):
    """Страница профиля другого пользователя"""
    other_user = get_object_or_404(User, id=user_id)
    
    # Проверяем, что пользователь не смотрит свой профиль
    if request.user == other_user:
        return redirect('profile')
    
    context = {
        'other_user': other_user,
    }
    return render(request, 'main/user_profile.html', context)


@login_required
@require_http_methods(["POST"])
def update_test_scores(request):
    """API для обновления баллов психологического теста"""
    try:
        # Пытаемся прочитать JSON; если не получилось, используем пустой dict
        try:
            data = json.loads(request.body or b"{}")
        except json.JSONDecodeError:
            data = {}
        user = request.user
        
        # Получаем новые значения вопросов (поддерживаем ключи q1..q5 и question1..question5,
        # а также form-encoded значения из request.POST)
        def pick_value(i: int):
            keys = [f"q{i}", f"question{i}"]
            for k in keys:
                if isinstance(data, dict) and k in data and data[k] is not None:
                    return data[k]
            for k in keys:
                if k in request.POST and request.POST.get(k):
                    return request.POST.get(k)
            return None

        q1 = pick_value(1)
        q2 = pick_value(2)
        q3 = pick_value(3)
        q4 = pick_value(4)
        q5 = pick_value(5)

        # Валидация входящих значений (должны быть целыми 1..5). Отсутствующие значения пропускаем
        def validate_optional(val, name):
            if val is None or val == "":
                return None
            try:
                ival = int(val)
            except (TypeError, ValueError):
                raise ValueError(f"{name} должен быть целым числом")
            if ival < 1 or ival > 5:
                raise ValueError(f"{name} должен быть от 1 до 5")
            return ival

        q1 = validate_optional(q1, 'q1')
        q2 = validate_optional(q2, 'q2')
        q3 = validate_optional(q3, 'q3')
        q4 = validate_optional(q4, 'q4')
        q5 = validate_optional(q5, 'q5')
        
        # Отладочная информация
        print(f"📊 Полученные данные: q1={q1}, q2={q2}, q3={q3}, q4={q4}, q5={q5}")
        print(f"📊 Старые значения пользователя: q1={user.question1}, q2={user.question2}, q3={user.question3}, q4={user.question4}, q5={user.question5}")
        
        # Обновляем баллы с помощью нового метода
        new_score = user.update_test_scores(q1=q1, q2=q2, q3=q3, q4=q4, q5=q5)
        
        print(f"📊 Новый общий балл: {new_score}")
        print(f"📊 Обновленные значения: q1={user.question1}, q2={user.question2}, q3={user.question3}, q4={user.question4}, q5={user.question5}")
        
        return JsonResponse({
            'status': 'success',
            'message': 'Баллы теста обновлены',
            'new_score': new_score,
            'q1': user.question1,
            'q2': user.question2,
            'q3': user.question3,
            'q4': user.question4,
            'q5': user.question5,
        })
        
    
    except ValueError as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Ошибка: {str(e)}'
        }, status=500)


def index_view(request):
    """Главная страница - редирект"""
    if request.user.is_authenticated:
        return redirect('profile')
    return redirect('auth')
