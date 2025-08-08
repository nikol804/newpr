from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class EmailOrUsernameModelBackend(ModelBackend):
    """
    Кастомный backend для аутентификации по email или username
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        login_identifier = username or kwargs.get(User.USERNAME_FIELD)
        if not login_identifier or not password:
            return None

        # Ищем по username или email без исключений
        user = User.objects.filter(Q(username__iexact=login_identifier) | Q(email__iexact=login_identifier)).first()
        if not user:
            # Митигируем timing attacks
            dummy = User()
            dummy.set_password(password)
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None
