# Task Manager API

A REST API built with FastAPI, PostgreSQL, and JWT authentication.

## Features
- User registration and login
- JWT token authentication
- Full task CRUD — create, read, update, delete
- Each user only sees their own tasks

## Tech Stack
- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy
- bcrypt + JWT

## Setup

1. Clone the repo
2. Create a virtual environment
```bash
   python -m venv venv
   source venv/Scripts/activate
```
3. Install dependencies
```bash
   pip install -r requirements.txt
```
4. Create a `.env` file
Add the following ...
```bash
    DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/taskmanager
    SECRET_KEY=yoursecretkey
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. Run the server
```bash
   uvicorn app.main:app --reload
```
6. Visit `http://localhost:8000/docs`

## Endpoints
| Method | Route | Auth | Description |
|--------|-------|------|-------------|
| POST | /register | No | Create account |
| POST | /login | No | Get token |
| GET | /tasks | Yes | Get all tasks |
| POST | /tasks | Yes | Create task |
| PUT | /tasks/{id} | Yes | Update task |
| DELETE | /tasks/{id} | Yes | Delete task |