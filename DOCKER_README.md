# 🐳 MatchMaker - Запуск в Docker

## 🚀 Быстрый запуск

### Windows:
```bash
.\docker-start.bat
```

### Linux/Mac:
```bash
chmod +x docker-start.sh
./docker-start.sh
```

### Ручной запуск:
```bash
docker-compose up --build
```

## 📱 После запуска

1. **Откройте браузер**: http://localhost:8000
2. **Тестовые пользователи**:
   - `test` / `123456`
   - `kola` / `123456`

## 🔧 Что включено в Docker

- **Django** с Daphne сервером (WebSocket + HTTP)
- **Redis** для real-time чата
- **Автоматические миграции** БД
- **Загрузка тестовых данных**
- **Поддержка nginx** для production (опционально)

## 🌟 Функции real-time чата

### Тройная система подключения:
1. **🟢 WebSocket** - мгновенные сообщения
2. **🔥 SSE (Server-Sent Events)** - real-time потоки  
3. **⚡ HTTP Polling** - быстрый fallback (500ms)

### Индикаторы в заголовке чата:
- **🟢 "Онлайн"** = WebSocket активен
- **🔥 "Real-time"** = SSE подключен
- **🟡 "HTTP режим"** = Быстрый polling

## 🛠️ Отладка

### Просмотр логов:
```bash
docker-compose logs -f web
docker-compose logs -f redis
```

### Подключение к контейнеру:
```bash
docker exec -it matchmaker_web bash
```

### Перезапуск отдельного сервиса:
```bash
docker-compose restart web
docker-compose restart redis
```

## 🔥 Production запуск с Nginx

```bash
docker-compose --profile production up
```

Это добавит nginx reverse proxy на порту 80.

## 📊 Проверка WebSocket в консоли

Откройте **Developer Tools (F12)** → **Console**:

**Ожидаемые логи при успешном WebSocket:**
```
🚀 Инициализация real-time чата...
🔗 WebSocket connect: chat_id=1, user=test
✅ WebSocket подключен - реальный чат активен!
```

**При fallback на SSE:**
```
🚀 Инициализация real-time чата...
❌ WebSocket ошибка: ...
🔗 Попытка подключения SSE...
✅ SSE подключен - реальный чат активен!
```

## 🛑 Остановка

```bash
docker-compose down
```

Или нажмите **Ctrl+C** в терминале.

---

## 💡 Особенности Docker версии

✅ **Изолированная среда** - никаких конфликтов с локальной системой  
✅ **Автоматический Redis** - сразу готов для WebSocket  
✅ **Единый запуск** - одна команда для всего  
✅ **Production готовность** - nginx конфиг включен  
✅ **Persistent данные** - Redis и медиа файлы сохраняются
