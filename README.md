# FastAPI Application with Docker

This project is a FastAPI application containerized using Docker and managed with Docker Compose. It includes a PostgreSQL database, a Redis instance for Celery, and a Celery worker.

## Folder Structure

The project follows a structured layout to separate concerns:

```
/
├───.gitignore
├───docker-compose.yml
├───Dockerfile
├───README.md
├───requirements.txt
├───.git/...
└───app/
    ├───__init__.py
    ├───celery_worker.py
    ├───main.py
    ├───__pycache__/
    ├───api/
    │   └───v1/
    │       └───endpoints/
    │           ├───auth.py
    │           └───__pycache__/
    ├───core/
    │   ├───config.py
    │   ├───dependencies.py
    │   ├───security.py
    │   └───__pycache__/
    ├───crud/
    │   ├───crud_user.py
    │   ├───crud_verification_code.py
    │   └───__pycache__/
    ├───db/
    │   ├───base.py
    │   ├───init_db.py
    │   ├───session.py
    │   └───__pycache__/
    ├───email_templates/
    │   └───welcome.html
    ├───models/
    │   ├───models.py
    │   └───__pycache__/
    ├───schemas/
    │   ├───schemas.py
    │   └───__pycache__/
    ├───services/
    │   ├───verification_code_service.py
    │   └───__pycache__/
    └───tests/
```

- **`app/`**: This directory contains the core FastAPI application code.
- **`Dockerfile`**: Defines the Docker image for the FastAPI application.
- **`docker-compose.yml`**: Defines the services, networks, and volumes for the application.
- **`requirements.txt`**: Lists the Python dependencies for the project.

## Prerequisites

Before you begin, ensure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

Follow these steps to get the application up and running:

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd fastapibackend
   ```

2. **Build and run the containers:**

   ```bash
   docker-compose up --build -d
   ```

   This command will build the Docker image for the FastAPI application and start the `web`, `db`, `redis`, and `worker` services in detached mode.

3. **Access the application:**

   Once the containers are running, you can access the FastAPI application at [http://localhost:8000/docs]
## Services

The `docker-compose.yml` file defines the following services:

- **`web`**: The FastAPI application, accessible at `http://localhost:8000`.
- **`db`**: The PostgreSQL database.
- **`redis`**: The Redis instance for Celery.
- **`worker`**: The Celery worker for background tasks.

## Environment Variables

The `docker-compose.yml` file uses environment variables to configure the PostgreSQL database and other settings. You can modify these variables as needed in the `docker-compose.yml` file or by creating a `.env` file.

## Dependencies

The project dependencies are managed with `pip` and listed in `requirements.txt`. Key dependencies include:

- `FastAPI`: Web framework for building APIs.
- `SQLAlchemy`: ORM for database interactions.
- `psycopg2-binary`: PostgreSQL adapter.
- `Celery`: Asynchronous task queue.
- `Redis`: Message broker for Celery.
- `python-jose`: For JWT authentication.
- `passlib[bcrypt]`: For password hashing.
- `uvicorn`: ASGI server.
- `alembic`: Database migrations.
- `email_validator`: For email validation.
