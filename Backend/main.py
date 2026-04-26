

from fastapi import FastAPI, Depends,HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, User

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
   return db.query(User).all()

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
def create_user(user: dict, db: Session = Depends(get_db)):
    new_user = User(
        name=user.get("name"),
        course=user.get("course"),
        skills=user.get("skills")
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully", "user": new_user}


@app.put("/users/{user_id}")
def update_user(user_id: int, updated_user: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in updated_user.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return {"message": "User updated successfully", "user": user}
    raise HTTPException(status_code=404, detail="User not found")


@app.patch("/users/{user_id}")
def partial_update_user(user_id: int, updated_fields: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in updated_fields.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return {"message": "User updated successfully", "user": user}