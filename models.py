from datetime import datetime

from pydantic import BaseModel


# ---------- Course schemas ----------

class Course(BaseModel):
    title: str
    code: str
    term: str
    description: str


class CourseResponse(Course):
    id: int

    class Config:
        from_attributes = True


# ---------- Document schemas ----------

class DocumentCreate(BaseModel):
    title: str


class DocumentResponse(BaseModel):
    id: int
    title: str
    filename: str
    uploaded_at: datetime
    course_id: int

    class Config:
        from_attributes = True