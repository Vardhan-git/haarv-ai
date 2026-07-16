from fastapi import FastAPI
from models import Course
from database_models import Base
from config import engine
from fastapi import Depends
from sqlalchemy.orm import Session
from config import session
from database_models import CourseDB
Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

@app.post("/courses", status_code=201)
def create_course(course: Course, db: Session = Depends(get_db)):
    new_course = CourseDB(
        title=course.title,
        code=course.code,
        term=course.term,
        description=course.description
    )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course



@app.get("/")
def greet():
    return "Welcome to Haarv AI"