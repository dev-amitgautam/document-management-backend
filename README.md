# Document Management System Backend

This is the backend for the Document Management System, built with FastAPI.

## Features

- User authentication and authorization with JWT
- Role-based access control (Admin, Editor, Viewer)
- Document management (upload, update, delete)
- Document ingestion process management
- RESTful API design

## Tech Stack

- FastAPI: Modern, fast web framework for building APIs
- SQLAlchemy: SQL toolkit and ORM
- PostgreSQL: Relational database
- Pydantic: Data validation and settings management
- JWT: Authentication mechanism
- Docker: Containerization

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.9+ (for local development)

### Running with Docker

1. Clone the repository
2. Navigate to the project directory
3. Run the application with Docker Compose:

```bash
docker-compose up --build
```

### Running Locally

1. Clone the repository
2. Navigate to the project directory
3. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Set up environment variables or create a `.env` file with:

```
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=document_management
SECRET_KEY=your-secret-key-for-jwt
```

6. Run the application:

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

## API Documentation

Once the application is running, you can access:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── dependencies.py
│   │   ├── routes/
│   │       ├── auth.py
│   │       ├── users.py
│   │       ├── documents.py
│   │       └── ingestion.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── exceptions.py
│   ├── db/
│   │   ├── database.py
│   │   └── repositories/
│   ├── models/
│   │   ├── user.py
│   │   ├── document.py
│   │   └── ingestion.py
│   ├── schemas/
│   │   ├── user.py
│   │   ├── document.py
│   │   └── ingestion.py
│   ├── services/
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── document.py
│   │   └── ingestion.py
│   └── main.py
├── uploads/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

This completes the backend implementation with all the necessary components for a well-structured FastAPI application that handles user authentication, document management, and ingestion processes.


