from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from app import models
from app.database import get_db
from app.auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter()


# --- Schemas ---

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_done: Optional[bool] = None
    due_date: Optional[datetime] = None


# --- Auth routes ---

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(data: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(
        (models.User.email == data.email) |
        (models.User.username == data.username)
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email or username already taken"
        )

    user = models.User(
        username=data.username,
        email=data.email,
        password=hash_password(data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "Account created", "username": user.username}


@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == data.email).first()

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


# --- Task routes ---

@router.get("/tasks")
def get_tasks(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    tasks = db.query(models.Task).filter(models.Task.owner_id == current_user.id).all()
    return tasks


@router.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(data: TaskCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    task = models.Task(
        title=data.title,
        description=data.description,
        due_date=data.due_date,
        owner_id=current_user.id
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.put("/tasks/{task_id}")
def update_task(task_id: int, data: TaskUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if data.title is not None:
        task.title = data.title
    if data.description is not None:
        task.description = data.description
    if data.is_done is not None:
        task.is_done = data.is_done
    if data.due_date is not None:
        task.due_date = data.due_date

    db.commit()
    db.refresh(task)
    return task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return