from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import engine, Base
from app.api.endpoints import students, subjects, grades

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Student Grades API",
    description="API pour gérer les élèves, les matières et les notes",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(students.router, prefix="/students", tags=["students"])
app.include_router(subjects.router, prefix="/subjects", tags=["subjects"])
app.include_router(grades.router, prefix="/grades", tags=["grades"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Student Grades API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)