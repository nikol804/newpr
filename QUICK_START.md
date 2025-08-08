# 🚀 Быстрый старт MatchMaker

## Windows

### Первый запуск:
1. Установите Python 3.8+ с https://python.org
2. Установите Redis с https://github.com/microsoftarchive/redis/releases
3. Запустите `setup.bat` - он установит все зависимости
4. Запустите Redis сервер (`redis-server.exe`)
5. Запустите `run.bat` - сервер стартует на http://127.0.0.1:8000

### Последующие запуски:
1. Запустите Redis сервер
2. Запустите `run.bat`

## Linux/Mac

### Первый запуск:
```bash
# Установите Redis
sudo apt-get install redis-server  # Ubuntu/Debian
brew install redis                  # Mac

# Настройте проект
chmod +x setup.sh run.sh
./setup.sh

# Запустите Redis
redis-server

# В новом терминале запустите сервер
./run.sh
```

### Последующие запуски:
1. Запустите `redis-server`
2. Запустите `./run.sh`

## 📱 Использование

1. Откройте http://127.0.0.1:8000
2. Зарегистрируйтесь (заполните тест и выберите минимум 3 интереса)
3. Перейдите в "Поиск" и нажмите "Найти собеседника"
4. Начните общение в чате!

## 🔧 Админ-панель

```bash
python manage.py createsuperuser
```
Доступ: http://127.0.0.1:8000/admin/

## ❓ Проблемы?

- **Порт 8000 занят**: Используйте `python manage.py runserver 8080`
- **Redis не запускается**: Проверьте порт 6379
- **Ошибки импорта**: Активируйте виртуальное окружение `venv\Scripts\activate` (Windows) или `source venv/bin/activate` (Linux/Mac)
