from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.db.database import get_db
from app.db.models import Grade, Student, Subject
from app.schemas.grade import Grade as GradeSchema, GradeCreate, GradeUpdate, GradeWithDetails

router = APIRouter()


@router.post("/", response_model=GradeSchema, status_code=status.HTTP_201_CREATED)
def create_grade(grade: GradeCreate, db: Session = Depends(get_db)):
    """Create a new grade for a student in a subject"""
    # Check if student exists
    student = db.query(Student).filter(Student.id == grade.student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    # Check if subject exists
    subject = db.query(Subject).filter(Subject.id == grade.subject_id).first()
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )
    
    db_grade = Grade(
        student_id=grade.student_id,
        subject_id=grade.subject_id,
        value=grade.value,
        comment=grade.comment
    )
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    return db_grade


@router.get("/", response_model=List[GradeWithDetails])
def read_grades(
    skip: int = 0, 
    limit: int = 100,
    min_grade: Optional[float] = None,
    max_grade: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """Get all grades with optional filtering"""
    query = db.query(Grade).options(
        joinedload(Grade.student),
        joinedload(Grade.subject)
    )
    
    if min_grade is not None:
        query = query.filter(Grade.value >= min_grade)
    
    if max_grade is not None:
        query = query.filter(Grade.value <= max_grade)
    
    grades = query.offset(skip).limit(limit).all()
    return grades


@router.get("/{grade_id}", response_model=GradeWithDetails)
def read_grade(grade_id: int, db: Session = Depends(get_db)):
    """Get a specific grade by ID"""
    db_grade = db.query(Grade).options(
        joinedload(Grade.student),
        joinedload(Grade.subject)
    ).filter(Grade.id == grade_id).first()
    
    if db_grade is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grade not found"
        )
    return db_grade


@router.get("/student/{student_id}", response_model=List[GradeWithDetails])
def read_student_grades(
    student_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all grades for a specific student"""
    # Check if student exists
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    grades = db.query(Grade).options(
        joinedload(Grade.student),
        joinedload(Grade.subject)
    ).filter(
        Grade.student_id == student_id
    ).offset(skip).limit(limit).all()
    
    return grades


@router.get("/subject/{subject_id}", response_model=List[GradeWithDetails])
def read_subject_grades(
    subject_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all grades for a specific subject"""
    # Check if subject exists
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )
    
    grades = db.query(Grade).options(
        joinedload(Grade.student),
        joinedload(Grade.subject)
    ).filter(
        Grade.subject_id == subject_id
    ).offset(skip).limit(limit).all()
    
    return grades


@router.put("/{grade_id}", response_model=GradeSchema)
def update_grade(
    grade_id: int,
    grade: GradeUpdate,
    db: Session = Depends(get_db)
):
    """Update a grade"""
    db_grade = db.query(Grade).filter(Grade.id == grade_id).first()
    if db_grade is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grade not found"
        )
    
    # Update only the fields that are provided
    update_data = grade.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_grade, key, value)
    
    db.commit()
    db.refresh(db_grade)
    return db_grade


@router.delete("/{grade_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_grade(grade_id: int, db: Session = Depends(get_db)):
    """Delete a grade"""
    db_grade = db.query(Grade).filter(Grade.id == grade_id).first()
    if db_grade is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grade not found"
        )
    
    db.delete(db_grade)
    db.commit()
    return None