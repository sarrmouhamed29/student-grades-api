# Student Grades API

Une API RESTful pour gérer les élèves, les matières et les notes, développée avec FastAPI et PostgreSQL.

## Fonctionnalités

- Gestion complète des élèves (CRUD)
- Gestion des matières (CRUD)
- Attribution et consultation des notes
- Calcul des moyennes par élève et par matière
- Documentation interactive avec Swagger UI

## Technologies utilisées

- **Backend**: FastAPI (Python)
- **Base de données**: PostgreSQL
- **ORM**: SQLAlchemy
- **Validation des données**: Pydantic
- **CI/CD**: GitHub Actions
- **Déploiement**: Railway

## Démarrage rapide

### Prérequis

- Python 3.9+
- PostgreSQL
- Git

### Installation locale

1. Cloner le dépôt
   ```bash
   git clone https://github.com/your-username/student-grades-api.git
   cd student-grades-api
   ```

2. Créer et activer un environnement virtuel
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows : venv\Scripts\activate
   ```

3. Installer les dépendances
   ```bash
   pip install -r requirements.txt
   ```

4. Configurer les variables d'environnement
   ```bash
   cp .env.example .env
   # Modifier les valeurs dans .env selon votre configuration PostgreSQL
   ```

5. Lancer l'application
   ```bash
   uvicorn app.main:app --reload
   ```

6. Accéder à l'application et à la documentation
   - API: http://localhost:8000/
   - Documentation Swagger: http://localhost:8000/docs

## API Endpoints

### Gestion des élèves
- `POST /students` - Ajouter un élève
- `GET /students` - Lister les élèves
- `GET /students/{id}` - Détails d'un élève
- `PUT /students/{id}` - Mettre à jour un élève
- `DELETE /students/{id}` - Supprimer un élève
- `GET /students/{id}/average` - Moyenne générale d'un élève

### Gestion des matières
- `POST /subjects` - Ajouter une matière
- `GET /subjects` - Lister les matières
- `GET /subjects/{id}` - Détails d'une matière
- `PUT /subjects/{id}` - Mettre à jour une matière
- `DELETE /subjects/{id}` - Supprimer une matière
- `GET /subjects/{id}/average` - Moyenne par matière

### Attribution des notes
- `POST /grades` - Attribuer une note
- `GET /grades` - Lister toutes les notes
- `GET /grades/{id}` - Détails d'une note
- `PUT /grades/{id}` - Mettre à jour une note
- `DELETE /grades/{id}` - Supprimer une note
- `GET /grades/student/{student_id}` - Notes d'un élève
- `GET /grades/subject/{subject_id}` - Notes d'une matière

## Déploiement sur Railway

### Configuration manuelle

1. Créer un compte sur [Railway](https://railway.app)
2. Créer un nouveau projet et lier votre dépôt GitHub
3. Ajouter un service PostgreSQL au projet
4. Définir les variables d'environnement nécessaires

### Déploiement automatique via GitHub Actions

1. Obtenir un token API Railway depuis les paramètres de votre compte
2. Ajouter le token comme secret GitHub nommé `RAILWAY_TOKEN`
3. Pousser sur la branche `main` pour déclencher le déploiement automatique

## Tests

Fonctionne comme prévu en local 
domain railway (a tester) student-grades-api-production-338e.up.railway.app

## Licence

MIT