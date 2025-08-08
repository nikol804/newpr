@echo off
echo ========================================
echo MatchMaker - Запуск WebSocket сервера
echo ========================================
echo.

echo Активируем виртуальное окружение...
call venv\Scripts\activate

echo.
echo Запускаем сервер с поддержкой WebSocket...
echo URL: http://127.0.0.1:8000
echo.
echo Тестовые пользователи:
echo   Никнейм: test   / Пароль: 123456
echo   Никнейм: kola   / Пароль: 123456
echo.
echo Для остановки нажмите Ctrl+C
echo ========================================
echo.

daphne -b 0.0.0.0 -p 8000 matchmaker.asgi:application
