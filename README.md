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

---

Регистрация/аутентификация:
- Для проверки регистрации (поле email в качестве username field) доступен эндпоинт:
<img width="591" height="473" alt="Снимок экрана 2025-09-23 в 12 02 21" src="https://github.com/user-attachments/assets/7aaa5f3f-2876-4142-9bac-cfda7fc1184f" />

- После регистрации аутентифицируйтесь:
<img width="562" height="497" alt="Снимок экрана 2025-09-23 в 12 02 47" src="https://github.com/user-attachments/assets/90fa296b-040b-4f9a-9201-f3945ddff959" />

- Скопируйте access token, который пришёл в ответе:
<img width="1275" height="212" alt="Снимок экрана 2025-09-23 в 12 03 33" src="https://github.com/user-attachments/assets/861824f4-f06b-42d0-983a-1546e1a70546" />

- Аутентификация для проверки в swagger - Authorize (правый верхний угол). Вставьте access toker в таком формате: `Bearer <ваш-access-токен>`
<img width="741" height="394" alt="Снимок экрана 2025-09-23 в 12 04 03" src="https://github.com/user-attachments/assets/c12e231e-0a92-4c4d-acd2-5cacaa02bac3" />

---

- Swagger - http://127.0.0.1:8000/swagger/
- UI DRF - http://127.0.0.1:8000/api/v1/ (http://127.0.0.1:8000/api/v1/collections/ и http://127.0.0.1:8000/api/v1/collections/500/payments/)
- UI Mailhog (локальный SMTP) - http://localhost:8025/
