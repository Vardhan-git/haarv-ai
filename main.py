from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from models import Course, CourseResponse, DocumentCreate, DocumentResponse
from database_models import Base, CourseDB, DocumentDB
from config import engine, session

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def greet():
    return "Welcome to Haarv AI"


# ---------- Courses ----------

@app.get("/courses", response_model=list[CourseResponse])
def get_courses(db: Session = Depends(get_db)):
    return db.query(CourseDB).all()


@app.get("/courses/{id}", response_model=CourseResponse)
def get_course_by_id(id: int, db: Session = Depends(get_db)):
    course = db.query(CourseDB).filter(CourseDB.id == id).first()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@app.post("/courses", response_model=CourseResponse, status_code=201)
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


@app.put("/courses/{id}", response_model=CourseResponse)
def update_course(id: int, course: Course, db: Session = Depends(get_db)):
    db_course = db.query(CourseDB).filter(CourseDB.id == id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    db_course.title = course.title
    db_course.code = course.code
    db_course.term = course.term
    db_course.description = course.description
    db.commit()
    db.refresh(db_course)
    return db_course


@app.delete("/courses/{id}", status_code=204)
def delete_course(id: int, db: Session = Depends(get_db)):
    db_course = db.query(CourseDB).filter(CourseDB.id == id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(db_course)
    db.commit()


# ---------- Documents ----------

@app.post("/courses/{course_id}/documents", response_model=DocumentResponse, status_code=201)
def add_document(course_id: int, document: DocumentCreate, db: Session = Depends(get_db)):
    course = db.query(CourseDB).filter(CourseDB.id == course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    new_document = DocumentDB(
        title=document.title,
        filename="placeholder.pdf",
        course_id=course_id
    )
    db.add(new_document)
    db.commit()
    db.refresh(new_document)
    return new_document


@app.get("/courses/{course_id}/documents", response_model=list[DocumentResponse])
def get_documents(course_id: int, db: Session = Depends(get_db)):
    course = db.query(CourseDB).filter(CourseDB.id == course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course.documents