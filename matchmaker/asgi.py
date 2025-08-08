"""
ASGI config for matchmaker project.
"""

import os

# Устанавливаем настройки Django ПЕРВЫМ
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'matchmaker.settings')

# Импортируем Django настройки
import django
django.setup()

# Теперь импортируем все остальное
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from main import routing

# Создаем Django ASGI приложение ПОСЛЕ импорта routing
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": URLRouter(
        routing.websocket_urlpatterns
    ),
})
