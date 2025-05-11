import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Charger les variables d'environnement du fichier .env (en développement local)
load_dotenv()

# Priorité à DATABASE_URL (fourni par Railway)
DATABASE_URL = os.getenv("DATABASE_URL")

# Si DATABASE_URL n'est pas trouvé, essayer DATABASE_PUBLIC_URL
if not DATABASE_URL:
    DATABASE_URL = os.getenv("DATABASE_PUBLIC_URL")

# Si aucun des deux n'est disponible, construire l'URL à partir des variables individuelles
if not DATABASE_URL:
    POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_SERVER = os.getenv("PGHOST") or os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT = os.getenv("PGPORT") or os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB = os.getenv("POSTGRES_DB") or os.getenv("PGDATABASE", "student_grades_db")
    
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Afficher l'URL de la base de données (sans le mot de passe) pour le débogage
safe_url = DATABASE_URL.replace(os.getenv("POSTGRES_PASSWORD", ""), "****") if os.getenv("POSTGRES_PASSWORD") else DATABASE_URL
print(f"Connecting to database: {safe_url}")

# Créer le moteur SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dépendance pour obtenir la session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()