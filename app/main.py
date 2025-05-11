from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.db.database import engine, Base
from app.api.endpoints import students, subjects, grades

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
    # Afficher des informations sur l'environnement pour le débogage
    db_url = os.getenv("DATABASE_URL", "Not set")
    if db_url and len(db_url) > 20:
        db_url = db_url[:10] + "..." + db_url[-10:]
        
    return {
        "message": "Welcome to Student Grades API",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "database_connected": db_url != "Not set"
    }

@app.on_event("startup")
async def startup_db_client():
    # Créer les tables de la base de données au démarrage
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error creating database tables: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=int(os.getenv("PORT", "8000")), reload=True)