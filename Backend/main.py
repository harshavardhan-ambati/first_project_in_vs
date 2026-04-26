

from fastapi import FastAPI, Depends,HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, User
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    course: str
    skills: str

class UserUpdate(BaseModel):
    name: str = None
    course: str = None
    skills: str = None

app = FastAPI()
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Welcome to vedhashreeu technology solutions"}

@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
   users = db.query(User).all()
   return users

@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.name == user.name).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this name already exists")
    new_user = User(name=user.name, course=user.course, skills=user.skills
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully", "user": new_user}


@app.put("/users/{user_id}")
def update_user(user_id: int, updated_user: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    existing_user = db.query(User).filter(User.name == updated_user.name, User.id != user_id).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this name already exists")
    user.name = updated_user.name
    user.course = updated_user.course
    user.skills = updated_user.skills
    db.commit()
    db.refresh(user)
    return {"message": "User updated successfully", "user": user}
    


@app.patch("/users/{user_id}")
def patch_user(user_id: int, updated_user: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if updated_user.name:
        existing_user = db.query(User).filter(User.name == updated_user.name, User.id != user_id).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this name already exists")
    if updated_user.name:
        user.name = updated_user.name
    if updated_user.course:
        user.course = updated_user.course
    if updated_user.skills:
        user.skills = updated_user.skills
    db.commit()
    db.refresh(user)
    return {"message": "User updated successfully", "user": user}