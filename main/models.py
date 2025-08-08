from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class Interest(models.Model):
    """Модель интересов пользователей"""
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    icon = models.CharField(max_length=50, default='fa-star', verbose_name='Иконка FontAwesome')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Интерес'
        verbose_name_plural = 'Интересы'
        ordering = ['name']


class User(AbstractUser):
    """Расширенная модель пользователя"""
    username = models.CharField(max_length=150, unique=True, verbose_name='Никнейм')
    email = models.EmailField(unique=True, verbose_name='Email')
    social_url = models.URLField(blank=True, null=True, verbose_name='Ссылка на соцсеть (VK и др.)')
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    interests = models.ManyToManyField(Interest, blank=True, related_name='users', verbose_name='Интересы')
    test_score = models.IntegerField(default=0, verbose_name='Результат теста')
    is_searching = models.BooleanField(default=False, verbose_name='В поиске')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    
    # Психологический тест - 5 вопросов
    question1 = models.IntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Насколько вы общительны?'
    )
    question2 = models.IntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Насколько вы открыты новому опыту?'
    )
    question3 = models.IntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Насколько вы эмоциональны?'
    )
    question4 = models.IntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Насколько вы организованны?'
    )
    question5 = models.IntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Насколько вы доброжелательны?'
    )
    
    def calculate_test_score(self):
        """Вычисляет общий балл теста"""
        self.test_score = self.question1 + self.question2 + self.question3 + self.question4 + self.question5
        return self.test_score
    
    def update_test_scores(self, q1=None, q2=None, q3=None, q4=None, q5=None):
        """Обновляет баллы психологического теста"""
        print(f"🔧 update_test_scores вызван с: q1={q1}, q2={q2}, q3={q3}, q4={q4}, q5={q5}")
        
        if q1 is not None:
            self.question1 = q1
            print(f"✅ Обновлен q1: {q1}")
        if q2 is not None:
            self.question2 = q2
            print(f"✅ Обновлен q2: {q2}")
        if q3 is not None:
            self.question3 = q3
            print(f"✅ Обновлен q3: {q3}")
        if q4 is not None:
            self.question4 = q4
            print(f"✅ Обновлен q4: {q4}")
        if q5 is not None:
            self.question5 = q5
            print(f"✅ Обновлен q5: {q5}")
        
        # Пересчитываем общий балл
        old_score = self.test_score
        self.calculate_test_score()
        print(f"🔢 Балл изменился с {old_score} на {self.test_score}")
        
        self.save()
        return self.test_score
    
    def save(self, *args, **kwargs):
        self.calculate_test_score()
        super().save(*args, **kwargs)
    
    def find_match(self):
        """Находит подходящего собеседника"""
        from django.db.models import Count, Q
        
        # Исключаем себя и тех, кто не в поиске
        potential_matches = User.objects.exclude(id=self.id).filter(is_searching=True)
        
        # Фильтруем по интересам (минимум 3 общих)
        my_interests = self.interests.all()
        if my_interests:
            potential_matches = potential_matches.filter(
                interests__in=my_interests
            ).annotate(
                common_interests=Count('interests', distinct=True)
            ).filter(common_interests__gte=3)
        
        # Фильтруем по результатам теста (разница не более 10 баллов)
        min_score = self.test_score - 10
        max_score = self.test_score + 10
        potential_matches = potential_matches.filter(
            test_score__gte=min_score,
            test_score__lte=max_score
        )
        
        # Возвращаем первого подходящего
        return potential_matches.first()
    
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'



