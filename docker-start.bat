@echo off
echo ========================================
echo MatchMaker - Запуск в Docker
echo ========================================
echo.

echo 🐳 Останавливаем предыдущие контейнеры...
docker-compose down

echo.
echo 🔨 Собираем и запускаем контейнеры...
docker-compose up --build

echo.
echo 🎉 MatchMaker готов!
echo 📱 Откройте: http://localhost:8000
echo 👤 Тестовые данные: test / 123456 или kola / 123456
echo.
echo Для остановки нажмите Ctrl+C
pause
