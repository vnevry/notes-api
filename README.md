# Notes API

REST API для управления заметками на Flask + SQLAlchemy.

## Стек
- Python 3.14, Flask, Flask-SQLAlchemy, Flask-CORS
- SQLite (локально), Gunicorn + Render (прод)

## Локальный запуск

    git clone https://github.com/vnevry/notes-api.git
    cd notes-api
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    python app.py

Сервер: http://127.0.0.1:5000

## Эндпоинты

| Метод  | URL                | Описание            |
|--------|--------------------|---------------------|
| GET    | /                  | Проверка работы     |
| GET    | /api/notes         | Список (пагинация, поиск) |
| GET    | /api/notes/:id     | Одна заметка        |
| POST   | /api/notes         | Создать             |
| PUT    | /api/notes/:id     | Обновить            |
| DELETE | /api/notes/:id     | Удалить             |

## Примеры curl

    curl -X POST http://127.0.0.1:5000/api/notes -H "Content-Type: application/json" -d "{\"title\":\"Заметка\",\"content\":\"Текст\"}"
    curl http://127.0.0.1:5000/api/notes
    curl http://127.0.0.1:5000/api/notes/1
    curl -X PUT http://127.0.0.1:5000/api/notes/1 -H "Content-Type: application/json" -d "{\"title\":\"Обновлено\"}"
    curl -X DELETE http://127.0.0.1:5000/api/notes/1

## Тесты

    pytest -v

## Демо

Проект развёрнут на Render: https://notes-api-hse8.onrender.com

Проверка:
curl https://notes-api-hse8.onrender.com/api/notes

## Автор

vnevry
