from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.database import get_db
from app.db.models import Subject, Grade
from app.schemas.subject import Subject as SubjectSchema, SubjectCreate, SubjectUpdate
from app.schemas.grade import SubjectAverage

router = APIRouter()


@router.post("/", response_model=SubjectSchema, status_code=status.HTTP_201_CREATED)
def create_subject(subject: SubjectCreate, db: Session = Depends(get_db)):
    """Create a new subject"""
    db_subject = db.query(Subject).filter(Subject.name == subject.name).first()
    if db_subject:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Subject already exists"
        )
    
    db_subject = Subject(
        name=subject.name,
        description=subject.description
    )
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject


@router.get("/", response_model=List[SubjectSchema])
def read_subjects(
    skip: int = 0, 
    limit: int = 100, 
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all subjects with optional search"""
    query = db.query(Subject)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Subject.name.ilike(search_term)) | 
            (Subject.description.ilike(search_term))
        )
    
    subjects = query.offset(skip).limit(limit).all()
    return subjects


@router.get("/{subject_id}", response_model=SubjectSchema)
def read_subject(subject_id: int, db: Session = Depends(get_db)):
    """Get a specific subject by ID"""
    db_subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if db_subject is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )
    return db_subject


@router.put("/{subject_id}", response_model=SubjectSchema)
def update_subject(
    subject_id: int, 
    subject: SubjectUpdate,
    db: Session = Depends(get_db)
):
    """Update a subject"""
    db_subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if db_subject is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )
    
    # Update only the fields that are provided
    update_data = subject.dict(exclude_unset=True)
    
    # If name is updated, check if the new name already exists
    if "name" in update_data and update_data["name"] != db_subject.name:
        existing_name = db.query(Subject).filter(Subject.name == update_data["name"]).first()
        if existing_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Subject name already exists"
            )
    
    for key, value in update_data.items():
        setattr(db_subject, key, value)
    
    db.commit()
    db.refresh(db_subject)
    return db_subject


@router.delete("/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    """Delete a subject"""
    db_subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if db_subject is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )
    
    db.delete(db_subject)
    db.commit()
    return None


@router.get("/{subject_id}/average", response_model=SubjectAverage)
def get_subject_average(subject_id: int, db: Session = Depends(get_db)):
    """Calculate the average grade for a subject"""
    # First check if subject exists
    db_subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if db_subject is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )
    
    # Calculate the average
    result = db.query(func.avg(Grade.value)).filter(Grade.subject_id == subject_id).scalar()
    
    # Format the result
    average = result if result is not None else 0.0
    
    return SubjectAverage(
        subject_id=subject_id,
        subject_name=db_subject.name,
        average=round(average, 2)
    )