# Todo App

A RESTful API built with **FastAPI**, **SQLAlchemy**, and **SQLite** for managing todo tasks with user authentication via **JWT**.

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| FastAPI | Web framework |
| SQLAlchemy | ORM / Database management |
| SQLite | Database |
| Pydantic | Data validation |
| passlib + bcrypt | Password hashing |
| python-jose | JWT token generation |
| uvicorn | ASGI server |

---

## Features

- User registration and login with JWT authentication
- Full CRUD for todos (create, read, update, delete)
- Filter todos by priority
- Password hashing with bcrypt
- Modular structure: routers, schemas, models

---

## Project Structure

```
todo-app/
+-- main.py                   # FastAPI app entry point
+-- database.py               # Database engine and session config
+-- models.py                 # SQLAlchemy ORM models (User, Todos)
+-- routers/
¦   +-- auth.py               # Auth endpoints (register, login, users)
¦   +-- todos.py              # Todo CRUD endpoints
+-- schemas/
    +-- user_request.py       # Pydantic schema for user input
    +-- todo_request.py       # Pydantic schema for todo input
    +-- token_squema.py       # Pydantic schema for JWT token response
```

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd todo-app
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv

   # Windows
   .venv\Scripts\Activate.ps1

   # Linux / Mac
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn sqlalchemy pydantic starlette passlib "python-jose[cryptography]" "passlib[bcrypt]"
   ```

4. **Start the server:**
   ```bash
   uvicorn main:app --reload
   ```

The API will be available at: **http://127.0.0.1:8000**

Interactive docs (Swagger UI): **http://127.0.0.1:8000/docs**

---

## Authentication

The API uses **JWT Bearer tokens**. To access protected endpoints:

1. Register a user via `POST /auth/createuser`
2. Login via `POST /auth/token` to receive a token
3. Include the token in the `Authorization` header:
   ```
   Authorization: Bearer <your-token>
   ```

---

## API Endpoints

### Auth — `/auth`

#### `POST /auth/createuser` — Register a user

**Request body:**
```json
{
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "password": "secret123",
  "role": "user"
}
```

**Response `201`:**
```json
{
  "message": "User created successfully",
  "user": {
    "id": 1,
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "role": "user",
    "is_active": true
  }
}
```

---

#### `POST /auth/token` — Login and get JWT token

**Request (form-data):**

| Field    | Value     |
|----------|-----------|
| username | johndoe   |
| password | secret123 |

**Response `200`:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

#### `GET /auth/users` — List all users

**Response `200`:**
```json
[
  {
    "id": 1,
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "role": "user",
    "is_active": true
  }
]
```

---

#### `DELETE /auth/deleteuser/{user_id}` — Delete user by ID

**Response `200`:**
```json
{
  "message": "User with id 1 deleted successfully"
}
```

---

### Todos — `/todos`

#### `GET /todos/` — Get all todos

**Response `200`:**
```json
[
  {
    "id": 1,
    "title": "Buy groceries today",
    "description": "Buy milk, bread, and eggs at the supermarket",
    "priority": 2,
    "complete": false,
    "owner_id": 1
  }
]
```

---

#### `GET /todos/{todo_id}` — Get todo by ID

**Response `200`:**
```json
{
  "id": 1,
  "title": "Buy groceries today",
  "description": "Buy milk, bread, and eggs at the supermarket",
  "priority": 2,
  "complete": false,
  "owner_id": 1
}
```

**Response `404`:**
```json
{
  "detail": "Todo with id 99 not found"
}
```

---

#### `GET /todos/priority?todo_priority=2` — Get todos by priority

Priority must be between **1 and 6**.

**Response `200`:**
```json
[
  {
    "id": 1,
    "title": "Buy groceries today",
    "description": "Buy milk, bread, and eggs at the supermarket",
    "priority": 2,
    "complete": false,
    "owner_id": 1
  }
]
```

---

#### `POST /todos/createtodo` — Create a todo

**Request body:**
```json
{
  "title": "Call the doctor now",
  "description": "Schedule annual checkup appointment",
  "priority": 3,
  "complete": false
}
```

**Validation rules:**
- `title`: 10–50 characters
- `description`: 10–200 characters
- `priority`: 0–6
- `complete`: boolean (default `false`)

**Response `201`:**
```json
{
  "message": "Todo with id 2 created successfully",
  "todo": {
    "id": 2,
    "title": "Call the doctor now",
    "description": "Schedule annual checkup appointment",
    "priority": 3,
    "complete": false,
    "owner_id": null
  }
}
```

---

#### `PUT /todos/updatetodo/{todo_id}` — Update a todo

**Request body:** same fields as `createtodo`

**Response `200`:**
```json
{
  "message": "Todo with id 2 updated successfully",
  "todo": {
    "id": 2,
    "title": "Call the doctor now",
    "description": "Schedule annual checkup and bring test results",
    "priority": 3,
    "complete": true,
    "owner_id": null
  }
}
```

**Response `404`:**
```json
{
  "detail": "Todo with id 99 not found for updates"
}
```

---

#### `DELETE /todos/deletetodo/{todo_id}` — Delete a todo

**Response `200`:**
```json
{
  "message": "Todo with id 2 deleted successfully"
}
```

**Response `404`:**
```json
{
  "detail": "Todo with id 99 not found for deletion"
}
```

---

## Database Models

### User

| Column          | Type    | Description              |
|-----------------|---------|--------------------------|
| id              | Integer | Primary key              |
| username        | String  | Unique username          |
| first_name      | String  | First name               |
| last_name       | String  | Last name                |
| email           | String  | Unique email             |
| hashed_password | String  | Bcrypt hashed password   |
| role            | String  | User role                |
| is_active       | Boolean | Account status           |

### Todos

| Column      | Type    | Description              |
|-------------|---------|--------------------------|
| id          | Integer | Primary key              |
| title       | String  | Todo title               |
| description | String  | Todo description         |
| priority    | Integer | Priority (0–6)           |
| complete    | Boolean | Completion status        |
| owner_id    | Integer | Foreign key ? users.id   |

---

## License

MIT
