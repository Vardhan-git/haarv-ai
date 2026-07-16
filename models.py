from pydantic import BaseModel  

class Course(BaseModel):
    title: str
    code: str
    term: str
    description: str