import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Ne charger les variables d'environnement du fichier .env qu'en développement local
if os.getenv("ENVIRONMENT") != "production":
    load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Student Grades API"
    API_VERSION: str = "1.0.0"
    
    # Database settings
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "student_grades_db")
    
    # Priorité à DATABASE_URL si elle existe
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Si DATABASE_URL n'est pas explicitement défini, le construire à partir des variables individuelles
        if not self.DATABASE_URL:
            self.DATABASE_URL = f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        
        # Correction pour SQLAlchemy qui préfère postgresql:// à postgres://
        if self.DATABASE_URL.startswith("postgres://"):
            self.DATABASE_URL = self.DATABASE_URL.replace("postgres://", "postgresql://", 1)

    class Config:
        case_sensitive = True

settings = Settings()