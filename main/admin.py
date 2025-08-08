from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Interest


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Админка для пользователей"""
    list_display = ['username', 'email', 'social_url', 'test_score', 'is_searching', 'created_at']
    list_filter = ['is_searching', 'is_staff', 'is_active', 'created_at']
    search_fields = ['username', 'email', 'social_url']
    filter_horizontal = ['interests']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('interests', 'social_url', 'test_score', 'is_searching',
                      'question1', 'question2', 'question3', 'question4', 'question5')
        }),
    )


@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    """Админка для интересов"""
    list_display = ['name', 'icon']
    search_fields = ['name']
    ordering = ['name']



