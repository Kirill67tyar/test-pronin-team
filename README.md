# Test Pronin Team

склонируйте проект:
```
git clone https://github.com/Kirill67tyar/test-pronin-team.git
```
в корневой директории скопируйте в .env содержимое .env.example:
```
cp .env.example .env
```
запуск проекта:
```
make up
```
или
```
docker compose up --build -d
```
наполнить БД:
```
make populate_db
```
или
```
docker compose exec django-app python manage.py populate_db
```
- Swagger - http://127.0.0.1:8000/swagger/
- UI DRF - http://127.0.0.1:8000/api/v1/ (http://127.0.0.1:8000/api/v1/collections/ и http://127.0.0.1:8000/api/v1/collections/500/payments/)
- UI Mailhog (локальный SMTP) - http://localhost:8025/
