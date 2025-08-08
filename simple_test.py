#!/usr/bin/env python
"""
Простая проверка Redis и Django Channels
"""

import os
import sys
import django

# Настройка Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'matchmaker.settings')
django.setup()

def check_redis():
    """Проверяет подключение к Redis"""
    print("🔍 Проверка Redis подключения...")
    
    try:
        import redis
        r = redis.Redis(host='127.0.0.1', port=6379, db=0)
        r.ping()
        print("✅ Redis подключение успешно!")
        
        # Тестируем запись/чтение
        r.set('test_key', 'test_value')
        value = r.get('test_key')
        if value == b'test_value':
            print("✅ Redis запись/чтение работает!")
        r.delete('test_key')
        
        return True
    except Exception as e:
        print(f"❌ Ошибка Redis: {e}")
        return False

def check_channels():
    """Проверяет настройки Channels"""
    print("\n🔍 Проверка настроек Channels...")
    
    try:
        from django.conf import settings
        backend = settings.CHANNEL_LAYERS['default']['BACKEND']
        print(f"Backend: {backend}")
        
        if 'redis' in backend.lower():
            print("✅ Настроен Redis backend для Channels")
            
            # Тестируем channel layer
            import channels.layers
            channel_layer = channels.layers.get_channel_layer()
            print(f"Channel layer: {type(channel_layer).__name__}")
            
            return True
        else:
            print("⚠️ Используется InMemory backend")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка настроек: {e}")
        return False

def check_server():
    """Проверяет статус Django сервера"""
    print("\n🔍 Проверка Django сервера...")
    
    try:
        import requests
        response = requests.get('http://127.0.0.1:8000', timeout=3)
        if response.status_code == 200:
            print("✅ Django сервер работает!")
            return True
    except:
        pass
    
    # Альтернативная проверка через сокет
    import socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('127.0.0.1', 8000))
        sock.close()
        
        if result == 0:
            print("✅ Django сервер работает на порту 8000!")
            return True
        else:
            print("❌ Django сервер не отвечает на порту 8000")
            return False
    except Exception as e:
        print(f"❌ Ошибка проверки сервера: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Диагностика WebSocket чата MatchMaker")
    print("=" * 50)
    
    # Проверяем компоненты
    redis_ok = check_redis()
    channels_ok = check_channels()
    server_ok = check_server()
    
    print("\n" + "=" * 50)
    print("📊 РЕЗУЛЬТАТ ДИАГНОСТИКИ:")
    print(f"  Redis: {'✅ OK' if redis_ok else '❌ Проблема'}")
    print(f"  Channels: {'✅ OK' if channels_ok else '❌ Проблема'}")  
    print(f"  Django сервер: {'✅ OK' if server_ok else '❌ Проблема'}")
    
    if redis_ok and channels_ok and server_ok:
        print("\n🎉 ВСЕ РАБОТАЕТ! WebSocket чат готов!")
        print("🟢 Ожидайте статус 'Онлайн' в чате")
    elif server_ok:
        print("\n⚠️ Сервер работает, но есть проблемы с WebSocket")
        print("🟡 Чат будет работать в HTTP режиме")
    else:
        print("\n❌ Есть проблемы с сервером")
    
    print("\n📱 Откройте чат: http://127.0.0.1:8000")
    print("👤 Войдите с: test / 123456")
    print("🔍 Проверьте статус в заголовке чата")
