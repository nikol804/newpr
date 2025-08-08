from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Interest


class TestForm(forms.ModelForm):
    """Форма психологического теста"""
    
    class Meta:
        model = User
        fields = ['question1', 'question2', 'question3', 'question4', 'question5']
        widgets = {
            'question1': forms.NumberInput(attrs={'type': 'range', 'min': 1, 'max': 5, 'step': 1, 'class': 'form-range test-range'}),
            'question2': forms.NumberInput(attrs={'type': 'range', 'min': 1, 'max': 5, 'step': 1, 'class': 'form-range test-range'}),
            'question3': forms.NumberInput(attrs={'type': 'range', 'min': 1, 'max': 5, 'step': 1, 'class': 'form-range test-range'}),
            'question4': forms.NumberInput(attrs={'type': 'range', 'min': 1, 'max': 5, 'step': 1, 'class': 'form-range test-range'}),
            'question5': forms.NumberInput(attrs={'type': 'range', 'min': 1, 'max': 5, 'step': 1, 'class': 'form-range test-range'}),
        }
        labels = {
            'question1': '1. Насколько вы общительны?',
            'question2': '2. Насколько вы открыты новому опыту?',
            'question3': '3. Насколько вы эмоциональны?',
            'question4': '4. Насколько вы организованны?',
            'question5': '5. Насколько вы доброжелательны?',
        }
        help_texts = {
            'question1': '1 - интроверт, 5 - экстраверт',
            'question2': '1 - консервативный, 5 - открытый',
            'question3': '1 - спокойный, 5 - эмоциональный',
            'question4': '1 - спонтанный, 5 - организованный',
            'question5': '1 - критичный, 5 - доброжелательный',
        }


class SignUpForm(UserCreationForm):
    """Форма регистрации с психологическим тестом и интересами (слайдеры 1-5)"""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@email.com'
        })
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Выберите никнейм'
        })
    )

    social_url = forms.URLField(
        required=True,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://vk.com/username'
        }),
        label='Ссылка на соцсеть (VK/Telegram и т.д.)'
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите пароль'
        })
    )

    interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        required=True,
        label='Выберите ваши интересы (минимум 3)',
        help_text='Выберите минимум 3 интереса для лучшего подбора собеседников'
    )

    # Поля психологического теста: слайдеры
    question1 = forms.IntegerField(
        min_value=1, max_value=5, required=True, initial=3,
        widget=forms.NumberInput(attrs={'type': 'range', 'min': 1, 'max': 5, 'step': 1, 'class': 'form-range test-range'}),
        label='1. Насколько вы общительны?',
        help_text='1 - интроверт, 5 - экстраверт'
    )

    question2 = forms.IntegerField(
        min_value=1, max_value=5, required=True, initial=3,
        widget=forms.NumberInput(attrs={'type': 'range', 'min': 1, 'max': 5, 'step': 1, 'class': 'form-range test-range'}),
        label='2. Насколько вы открыты новому опыту?',
        help_text='1 - консервативный, 5 - открытый'
    )

    question3 = forms.IntegerField(
        min_value=1, max_value=5, required=True, initial=3,
        widget=forms.NumberInput(attrs={'type': 'range', 'min': 1, 'max': 5, 'step': 1, 'class': 'form-range test-range'}),
        label='3. Насколько вы эмоциональны?',
        help_text='1 - спокойный, 5 - эмоциональный'
    )

    question4 = forms.IntegerField(
        min_value=1, max_value=5, required=True, initial=3,
        widget=forms.NumberInput(attrs={'type': 'range', 'min': 1, 'max': 5, 'step': 1, 'class': 'form-range test-range'}),
        label='4. Насколько вы организованны?',
        help_text='1 - спонтанный, 5 - организованный'
    )

    question5 = forms.IntegerField(
        min_value=1, max_value=5, required=True, initial=3,
        widget=forms.NumberInput(attrs={'type': 'range', 'min': 1, 'max': 5, 'step': 1, 'class': 'form-range test-range'}),
        label='5. Насколько вы доброжелательны?',
        help_text='1 - критичный, 5 - доброжелательный'
    )
    
    class Meta:
        model = User
        fields = ['email', 'username', 'social_url', 'password1', 'password2', 'interests',
                  'question1', 'question2', 'question3', 'question4', 'question5']
    
    def clean_interests(self):
        interests = self.cleaned_data.get('interests')
        if interests and len(interests) < 3:
            raise forms.ValidationError('Выберите минимум 3 интереса')
        return interests
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Проверяем, что все вопросы теста отвечены
        questions = ['question1', 'question2', 'question3', 'question4', 'question5']
        for question in questions:
            if not cleaned_data.get(question):
                raise forms.ValidationError(f'Пожалуйста, ответьте на все вопросы теста')
        
        return cleaned_data
    
    def clean_social_url(self):
        url = self.cleaned_data.get('social_url', '').strip()
        if url and not (url.startswith('http://') or url.startswith('https://')):
            url = 'https://' + url
        return url

    def save(self, commit=True):
        # Создаем пользователя, явно устанавливая пароль и нормализуя поля
        user = super().save(commit=False)
        user.username = (self.cleaned_data.get('username') or '').strip()
        user.email = (self.cleaned_data.get('email') or '').strip()
        user.social_url = self.cleaned_data.get('social_url')

        # Устанавливаем пароль явно, чтобы избежать несоответствий
        password = self.cleaned_data.get('password1')
        if password:
            user.set_password(password)

        # Сохраняем ответы теста
        user.question1 = int(self.cleaned_data.get('question1', 3))
        user.question2 = int(self.cleaned_data.get('question2', 3))
        user.question3 = int(self.cleaned_data.get('question3', 3))
        user.question4 = int(self.cleaned_data.get('question4', 3))
        user.question5 = int(self.cleaned_data.get('question5', 3))

        if commit:
            user.save()
            if 'interests' in self.cleaned_data:
                user.interests.set(self.cleaned_data['interests'])
            user.calculate_test_score()
            user.save()

        return user


class LoginForm(AuthenticationForm):
    """Форма авторизации"""
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Никнейм или email'
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль'
        })
    )

    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        label='Запомнить меня',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


class ProfileUpdateForm(forms.ModelForm):
    """Форма обновления профиля"""
    
    interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        required=True,
        label='Ваши интересы'
    )
    
    class Meta:
        model = User
        fields = ['interests', 'social_url']
        widgets = {
            'social_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://vk.com/username'})
        }
        labels = {
            'social_url': 'Ссылка на соцсеть (VK/Telegram и т.д.)'
        }
    
    def clean_interests(self):
        interests = self.cleaned_data.get('interests')
        if interests and len(interests) < 3:
            raise forms.ValidationError('Выберите минимум 3 интереса')
        return interests