#!/usr/bin/env python
import os
import sys
import django

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'matchmaker.settings')
django.setup()

from main.models import User

# Получаем первого пользователя
user = User.objects.first()
if user:
    print(f"Пользователь: {user.username}")
    print(f"Текущие значения:")
    print(f"  question1: {user.question1}")
    print(f"  question2: {user.question2}")
    print(f"  question3: {user.question3}")
    print(f"  question4: {user.question4}")
    print(f"  question5: {user.question5}")
    print(f"  test_score: {user.test_score}")
    
    # Устанавливаем разные значения для теста
    user.question1 = 1
    user.question2 = 2
    user.question3 = 4
    user.question4 = 5
    user.question5 = 3
    user.calculate_test_score()
    user.save()
    
    print(f"\nОбновленные значения:")
    print(f"  question1: {user.question1}")
    print(f"  question2: {user.question2}")
    print(f"  question3: {user.question3}")
    print(f"  question4: {user.question4}")
    print(f"  question5: {user.question5}")
    print(f"  test_score: {user.test_score}")
else:
    print("Пользователей не найдено!")
