# Todo App

A RESTful API to manage todo tasks, built with FastAPI, SQLAlchemy, and SQLite.

## Features
- Create, read, update, and delete tasks (CRUD)
- Filter tasks by priority
- Data validation with Pydantic
- SQLite database ready to use

## Installation

1. Clone this repository:
   ```bash
   git clone <repo-url>
   cd todo-app
   ```
2. (Optional) Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # On Windows
   .venv\Scripts\activate
   # On Linux/Mac
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install fastapi uvicorn sqlalchemy pydantic starlette
   ```

## Usage

Start the development server:
```bash
uvicorn main:app --reload
```

The API will be available at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

Interactive documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Main Endpoints

### Get all todos
- **GET** `/mytodos`

#### Example response
```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "description": "Buy milk, bread, and eggs at the supermarket",
    "priority": 2,
    "complete": false
  }
]
```

### Get todo by ID
- **GET** `/mytodos/{todo_id}`

#### Example response
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Buy milk, bread, and eggs at the supermarket",
  "priority": 2,
  "complete": false
}
```

### Get todos by priority
- **GET** `/mytodos/priority/{todo_priority}`

#### Example response
```json
[
  {
    "id": 2,
    "title": "Study for the exam",
    "description": "Review math topics",
    "priority": 1,
    "complete": false
  }
]
```

### Create a todo
- **POST** `/mytodos/createtodo/`

#### Example request
```json
{
  "title": "Call the doctor",
  "description": "Schedule annual checkup appointment",
  "priority": 3,
  "complete": false
}
```

#### Example response
```json
{
  "message": "Todo with id 3 created successfully",
  "todo": {
    "id": 3,
    "title": "Call the doctor",
    "description": "Schedule annual checkup appointment",
    "priority": 3,
    "complete": false
  }
}
```

### Update a todo
- **PUT** `/mytodos/updatetodo/{todo_id}`

#### Example request
```json
{
  "title": "Call the doctor",
  "description": "Schedule annual checkup and bring test results",
  "priority": 3,
  "complete": true
}
```

#### Example response
```json
{
  "message": "Todo with id 3 updated successfully",
  "todo": {
    "id": 3,
    "title": "Call the doctor",
    "description": "Schedule annual checkup and bring test results",
    "priority": 3,
    "complete": true
  }
}
```

### Delete a todo
- **DELETE** `/mytodos/deletetodo/{todo_id}`

#### Example response
```json
{
  "message": "Todo with id 3 deleted successfully"
}
```

---

## Project structure

```
├── database.py         # Database configuration
├── main.py             # API endpoints and main logic
├── models.py           # Data model definition (ORM)
├── todo_request.py     # Request validation schema
└── ...
```

---

## License
MIT
