from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.database import get_db
from app.db.models import Student, Grade
from app.schemas.student import Student as StudentSchema, StudentCreate, StudentUpdate
from app.schemas.grade import StudentAverage

router = APIRouter()


@router.post("/", response_model=StudentSchema, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    """Create a new student"""
    db_student = db.query(Student).filter(Student.email == student.email).first()
    if db_student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    db_student = Student(
        first_name=student.first_name,
        last_name=student.last_name,
        email=student.email
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


@router.get("/", response_model=List[StudentSchema])
def read_students(
    skip: int = 0, 
    limit: int = 100, 
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all students with optional search"""
    query = db.query(Student)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Student.first_name.ilike(search_term)) | 
            (Student.last_name.ilike(search_term)) |
            (Student.email.ilike(search_term))
        )
    
    students = query.offset(skip).limit(limit).all()
    return students


@router.get("/{student_id}", response_model=StudentSchema)
def read_student(student_id: int, db: Session = Depends(get_db)):
    """Get a specific student by ID"""
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return db_student


@router.put("/{student_id}", response_model=StudentSchema)
def update_student(
    student_id: int, 
    student: StudentUpdate,
    db: Session = Depends(get_db)
):
    """Update a student's information"""
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    # Update only the fields that are provided
    update_data = student.dict(exclude_unset=True)
    
    # If email is updated, check if the new email already exists
    if "email" in update_data and update_data["email"] != db_student.email:
        existing_email = db.query(Student).filter(Student.email == update_data["email"]).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    for key, value in update_data.items():
        setattr(db_student, key, value)
    
    db.commit()
    db.refresh(db_student)
    return db_student


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    """Delete a student"""
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    db.delete(db_student)
    db.commit()
    return None


@router.get("/{student_id}/average", response_model=StudentAverage)
def get_student_average(student_id: int, db: Session = Depends(get_db)):
    """Calculate the overall average grade for a student"""
    # First check if student exists
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    # Calculate the average
    result = db.query(func.avg(Grade.value)).filter(Grade.student_id == student_id).scalar()
    
    # Format the result
    average = result if result is not None else 0.0
    
    return StudentAverage(
        student_id=student_id,
        student_name=f"{db_student.first_name} {db_student.last_name}",
        overall_average=round(average, 2)
    )