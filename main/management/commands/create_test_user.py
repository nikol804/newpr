from django.core.management.base import BaseCommand
from main.models import User, Interest


class Command(BaseCommand):
    help = 'Создает тестового пользователя для отладки'

    def handle(self, *args, **options):
        # Удаляем существующего тестового пользователя если есть
        User.objects.filter(username='test').delete()
        
        # Создаем нового тестового пользователя
        user = User.objects.create_user(
            username='test',
            email='test@test.com',
            password='test123',
            question1=3,
            question2=3,
            question3=3,
            question4=3,
            question5=3
        )
        
        # Добавляем интересы
        interests = Interest.objects.all()[:3]
        user.interests.set(interests)
        user.calculate_test_score()
        user.save()
        
        self.stdout.write(
            self.style.SUCCESS(f'Тестовый пользователь создан:')
        )
        self.stdout.write(f'Никнейм: test')
        self.stdout.write(f'Email: test@test.com')
        self.stdout.write(f'Пароль: test123')
        self.stdout.write(f'Балл теста: {user.test_score}')
        self.stdout.write(f'Интересы: {", ".join([i.name for i in user.interests.all()])}')
