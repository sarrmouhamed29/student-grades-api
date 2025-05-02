from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

from app.schemas.student import Student
from app.schemas.subject import Subject


class GradeBase(BaseModel):
    student_id: int
    subject_id: int
    value: float = Field(..., ge=0, le=20)  # Grade between 0 and 20
    comment: Optional[str] = None


class GradeCreate(GradeBase):
    pass


class GradeUpdate(BaseModel):
    value: Optional[float] = Field(None, ge=0, le=20)
    comment: Optional[str] = None


class Grade(GradeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class GradeWithDetails(Grade):
    student: Student
    subject: Subject

    class Config:
        orm_mode = True


class StudentAverage(BaseModel):
    student_id: int
    student_name: str
    overall_average: float


class SubjectAverage(BaseModel):
    subject_id: int
    subject_name: str
    average: float