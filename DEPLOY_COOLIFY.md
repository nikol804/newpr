Deploying Django project to Coolify (Docker Compose)

1) Предварительная подготовка
- Убедитесь, что в репозитории есть: `Dockerfile`, `docker-entrypoint.sh`, `docker-compose.yml`, `nginx.conf` и `requirements.txt`.
- В корне проекта разместите файл окружения `(.env)` или применяйте переменные через UI Coolify. Пример файла — `env.example` (не храните секреты в репозитории).
- В `docker-compose.yml` настроены два сервиса: `web` (Django + Daphne) и `db` (PostgreSQL), а также `nginx` как прокси.

2) Файлы окружения
- Склонируйте образцы: создайте `.env` на основе `env.example` и заполните:
  - DATABASE_HOST, DATABASE_PORT, DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD
  - DJANGO_SETTINGS_MODULE, SECRET_KEY, ALLOWED_HOSTS

3) Развёртывание в Coolify
- Создайте новый проект в Coolify и подключите репозиторий с кодом.
- Выберите способ развёртывания: Docker Compose (используйте файл `docker-compose.yml`).
- Укажите переменные окружения или загрузите файл `.env` через UI:
  - DATABASE_HOST=db
  - DATABASE_PORT=5432
  - DATABASE_NAME=coolifydb
  - DATABASE_USER=coolifyuser
  - DATABASE_PASSWORD=your_db_password
  - DJANGO_SETTINGS_MODULE=matchmaker.settings
  - SECRET_KEY=your_secret_key
  - DEBUG=False
  - ALLOWED_HOSTS=your.domain

4) Параметры и безопасность
- Выполните сборку образов и запуск через кнопки Deploy.
- Включите persistent volume для PostgreSQL (`postgres_data`).
- Убедитесь, что `SECURE_*` настройки применяются на продакшене (внедрить через nginx/параметры окружения).

5) Тестирование после развёртывания
- Проверить доступ по порту 80 (или настроенному домену).
- Войти как админ/пользователь и проверить: регистрация, вход, создание постов, комментарии, поиск.
- Прогнать миграции при первом запуске: `python manage.py migrate` (через Docker entrypoint).

6) Откат и обновления
- В Coolify можно откатить к предыдущему коммиту/контейнеру через UI.
- При изменениях в коде — повторить Deploy и проверить миграции/медиа-файлы.

7) Быстрые команды для локальной проверки
- Запуск локально: `docker-compose up -d`.
- Выполнить миграции: `docker-compose exec web python manage.py migrate`.
- Создать суперпользователя: `docker-compose exec web python manage.py createsuperuser`.

8) Контакты и подсказки
- Логи можно смотреть через Coolify или локально: `docker-compose logs -f`.
- Для безопасности держите SECRET_KEY и DB-пароли в секрете.


