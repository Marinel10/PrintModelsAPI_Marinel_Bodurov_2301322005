<div align="center">

# 🖨️ 3D Print Models REST API

**REST API за управление на модели за 3D печат, дизайнери, категории и материали**

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-REST_API-009688?logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-D71F00)
![Pydantic](https://img.shields.io/badge/Pydantic-2.x-E92063)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-Migrations-6BA539)

**Курсов проект** · **ФН: 2301322005**

</div>

---

## 📌 За проекта

Приложението предоставя REST API за съхранение и управление на 3D модели за печат. Всеки модел принадлежи на дизайнер, може да има категория и използва един или повече материали с определени количества и мерни единици.

API позволява:

- CRUD операции за **дизайнери**, **категории**, **материали** и **3D модели**.
- Свързване на материали с 3D модели, без да се дублират материалите.
- Филтриране на модели по име, категория и максимално време за печат с логика **AND**.
- Извличане на всички модели за даден дизайнер и всички материали за даден модел.
- Пропорционално изчисляване на необходимите материали за избран брой копия, **без промяна на записаните данни**.
- Валидация на входните данни и обработка на HTTP грешки.

## 🧱 Използвани технологии

| Технология | Предназначение |
|---|---|
| **Python 3.11** | Основен език |
| **FastAPI** | REST ендпойнти и Swagger документация |
| **Pydantic v2** | Валидация и схеми за заявките/отговорите |
| **SQLAlchemy 2.x** | ORM и работа с базата данни |
| **SQLite** | Релационна база данни |
| **Alembic** | Версиониране и прилагане на миграции |

## 🗂️ Структура на проекта

```text
PrintModelsAPI_Marinel_Bodurov_2301322005/
├── main.py                         # FastAPI приложение и обработка на грешки
├── exceptions.py                   # AppError, NotFound, ConflictError
├── requirements.txt                # Python зависимости
├── alembic.ini                     # Alembic конфигурация
├── alembic/
│   ├── env.py
│   └── versions/                  # Миграции на базата
├── db/
│   ├── database.py                 # Engine, SessionLocal, get_db
│   └── models/                     # SQLAlchemy ORM модели
│       ├── base.py
│       ├── designer.py
│       ├── category.py
│       ├── material.py
│       ├── print_model.py
│       └── print_model_material.py
├── models/                        # Pydantic Create / Update / Read
│   ├── designer.py
│   ├── category.py
│   ├── material.py
│   ├── print_model.py
│   └── print_model_material.py
├── services/                       # Бизнес логика
│   ├── designer_service.py
│   ├── category_service.py
│   ├── material_service.py
│   ├── print_model_service.py
│   └── print_model_material_service.py
└── routers/                        # HTTP ендпойнти
    ├── designer.py
    ├── category.py
    ├── material.py
    ├── print_model.py
    └── print_model_material.py
```

> **Забележка:** `print_models.db`, `.venv/`, `__pycache__/` и другите локални/генерирани файлове не трябва да се качват в Git.

## 🚀 Инсталиране и стартиране

### 1. Клониране на проекта

```bash
git clone <URL-НА-РЕПОЗИТОРИТО>
cd PrintModelsAPI_Marinel_Bodurov_2301322005
```

### 2. Създаване на виртуална среда

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Инсталиране на зависимостите

```bash
python -m pip install -r requirements.txt
```

### 4. Прилагане на миграциите

```bash
python -m alembic upgrade head
```

Alembic създава необходимите таблици и прилага последващата миграция за `difficulty`. **Не е необходимо ръчно създаване на таблиците чрез `Base.metadata.create_all()`**.

Текущата версия на базата може да се провери с:

```bash
python -m alembic current
```

### 5. Стартиране на API

```bash
python -m uvicorn main:app --reload
```

API: **http://127.0.0.1:8000**

- **Swagger UI:** http://127.0.0.1:8000/docs
- **OpenAPI схема:** http://127.0.0.1:8000/openapi.json

За спиране: `Ctrl + C`.

## 🔌 Ендпойнти

### Основни CRUD операции

| Метод | Път | Описание |
|---|---|---|
| `GET` | `/designers/` | Всички дизайнери |
| `GET` | `/designers/{designer_id}` | Дизайнер по ID |
| `POST` | `/designers/` | Създаване на дизайнер |
| `PUT` | `/designers/{designer_id}` | Редактиране на дизайнер |
| `DELETE` | `/designers/{designer_id}` | Изтриване на дизайнер |
| `GET` / `POST` | `/categories/` | Списък / създаване на категория |
| `GET` / `PUT` / `DELETE` | `/categories/{category_id}` | Детайли / редактиране / изтриване |
| `GET` / `POST` | `/materials/` | Списък / създаване на материал |
| `GET` / `PUT` / `DELETE` | `/materials/{material_id}` | Детайли / редактиране / изтриване |
| `GET` / `POST` | `/print-models/` | Списък (с филтри) / създаване на модел |
| `GET` / `PUT` / `DELETE` | `/print-models/{print_model_id}` | Детайли / редактиране / изтриване |

### Специфични операции

| Метод | Път | Описание |
|---|---|---|
| `GET` | `/designers/{designer_id}/print-models` | Модели на конкретен дизайнер |
| `GET` | `/print-models/{print_model_id}/materials` | Материали, количества и мерни единици |
| `POST` | `/print-models/{print_model_id}/materials` | Добавяне на материал към модел |
| `PUT` | `/print-models/{print_model_id}/materials/{material_id}` | Промяна на количество / единица |
| `DELETE` | `/print-models/{print_model_id}/materials/{material_id}` | Премахване само на връзката |
| `GET` | `/print-models/{print_model_id}/recalculate?copies=N` | Изчисляване на материали за N копия |

### Филтриране

Параметрите на `GET /print-models/` са незадължителни и се комбинират с **AND** директно в SQL заявката.

```http
GET /print-models/?name=Dragon&category_id=1&max_print_time=180
```

## 🧪 Примерни заявки

### Създаване на дизайнер

`POST /designers/`

```json
{
  "name": "Ivan",
  "email": "ivan@example.com"
}
```

### Създаване на 3D модел

`POST /print-models/`

```json
{
  "name": "Dragon",
  "instructions": "Print with PLA",
  "print_time_minutes": 120,
  "copies": 2,
  "designer_id": 1,
  "category_id": 1,
  "difficulty": "medium"
}
```

> Посочените `designer_id` и `category_id` трябва да съществуват в базата. `category_id` може да бъде `null`.

### Добавяне на материал към модел

`POST /print-models/1/materials`

```json
{
  "material_id": 1,
  "quantity": 100,
  "unit": "g"
}
```

Допустими мерни единици: `g`, `m`, `ml`.

### Преизчисляване на материалите

```http
GET /print-models/1/recalculate?copies=5
```

Ако материалът изисква **100 g за едно копие**, за пет копия са необходими **500 g**:

```text
quantity_per_copy = 100 g
requested_copies = 5
required_quantity = 100 × 5 = 500 g
```

Преизчисляването **не променя** записаното количество, нито броя копия в SQLite.

## ✅ Бизнес правила

| Правило | Поведение |
|---|---|
| Имейлите на дизайнерите са уникални | Дубликат → `409 Conflict` |
| Имената на моделите са уникални в рамките на дизайнер | Дубликат → `409 Conflict` |
| Сравняването на имена игнорира регистъра и крайните интервали | Нормализация и проверки за уникалност |
| Един материал се добавя само веднъж към даден модел | Повторно добавяне → `409 Conflict` |
| Изтриване на модел | Премахва връзките с материали, запазва материалите |
| Изтриване на категория | Моделите се запазват с `category_id = NULL` |
| Изтриване на дизайнер с модели | `409 Conflict` |
| Изтриване на използван материал | `409 Conflict` |
| Несъществуващ основен ресурс при списък със свързани записи | `404 Not Found` |
| Съществуващ ресурс без свързани записи | `200 OK` и `[]` |

### Ограничение за копията

Последните две цифри на факултетния номер са **05**, следователно:

**50 + 5 = 55 максимално допустими копия** при преизчисляване.

Заявка с `copies=56` се отхвърля като невалиден вход. `copies` трябва да е положително цяло число.

### Трудност на модела

Полето `difficulty` допуска само:

`easy` · `medium` · `hard`

Проверката е реализирана както на ниво Pydantic, така и чрез ограничение в базата данни.

## 🗄️ База данни и Alembic

Проектът използва пет основни ORM модела:

- `Designer` — дизайнер и неговите модели (**1:N**).
- `Category` — категория и принадлежащите ѝ модели (**1:N**, категорията е незадължителна).
- `Material` — материал за печат.
- `PrintModel` — 3D модел, дизайнер, категория, инструкции, време, копия и трудност.
- `PrintModelMaterial` — междинна таблица за връзката **N:M**, количество и мерна единица.

Миграциите са отделни етапи:

1. **Начална миграция** — създаване на таблиците, връзките и ограниченията.
2. **Втора миграция** — добавяне на `difficulty` и ограничение за валидните стойности.


## 📋 HTTP статуси

| Статус | Значение |
|---|---|
| `200 OK` | Успешно извличане / редактиране |
| `201 Created` | Успешно създаване |
| `204 No Content` | Успешно изтриване |
| `400 Bad Request` | Невалидни данни, отхвърлени от Service |
| `404 Not Found` | Несъществуващ ресурс |
| `409 Conflict` | Дубликат или нарушено бизнес правило |
| `422 Unprocessable Entity` | Невалидни входни данни според FastAPI/Pydantic |

---

<div align="center">

**3D Print Models API** · FastAPI · SQLAlchemy · Alembic

*Курсов проект*

</div>
