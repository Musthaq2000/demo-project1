# Docker Compose PostgreSQL API

A production-style Docker Compose project that demonstrates how to containerize a Python API and connect it to PostgreSQL using Docker networking, environment variables, health checks, and persistent named volumes.

## Project overview

The stack contains two services:

- **api** — Python Flask API built from the included Dockerfile. It listens on port 8000 inside the container and is published on host port 8080.
- **db** — PostgreSQL 16 Alpine database with persistent storage on the named `pgdata` volume.

The API connects to PostgreSQL using the Compose service name `db` rather than `localhost`.

## Architecture

```text
                    Docker Compose network

  Client
    |
    | http://localhost:8080
    v
+---------------------+
| api                 |
| Python / Flask      |
| container :8000     |
+----------+----------+
           |
           | DB_HOST=db :5432
           v
+---------------------+
| db                  |
| PostgreSQL 16       |
| container :5432     |
+----------+----------+
           |
           v
+---------------------+
| pgdata              |
| Named Docker volume |
+---------------------+
```

## Project files

```text
Docker/
├── app.py
├── requirements.txt
├── Dockerfile
├── compose.yaml
└── README.md
```

## Dockerfile highlights

The Dockerfile:

1. Uses `python:3.12-slim`.
2. Sets `/app` as the working directory.
3. Copies `requirements.txt` before the application source to improve build-cache reuse.
4. Installs dependencies with pip.
5. Copies `app.py`.
6. Exposes port 8000.
7. Creates and switches to a non-root `appuser`.
8. Starts the application with Python by default.

## Compose highlights

The Compose file demonstrates:

- `build: .` for the API image.
- Host-to-container port mapping: `8080:8000`.
- Environment variables for database configuration.
- Service-name DNS using `DB_HOST: db`.
- PostgreSQL 16 Alpine.
- A named volume mounted at `/var/lib/postgresql/data`.
- `depends_on` with `condition: service_healthy`.
- A PostgreSQL readiness check using `pg_isready`.

## Start the stack

From this directory:

```bash
docker compose up -d --build
```

Check the services:

```bash
docker compose ps
```

The database should eventually show `healthy`.

## Test the API

Add orders:

```bash
curl http://localhost:8080/add
```

Run it multiple times to add multiple orders.

Check the count:

```bash
curl http://localhost:8080/count
```

Example:

```text
order added
order added
2
```

## Verify the API user

The API container runs as the non-root user created in the Dockerfile:

```bash
docker compose exec api whoami
```

Expected:

```text
appuser
```

## Verify the database volume

```bash
docker volume ls
```

Inspect the Compose volume:

```bash
docker volume inspect pgdata
```

The PostgreSQL data is stored in the named volume and survives normal container recreation.

## Logs

View all service logs:

```bash
docker compose logs
```

Follow API logs:

```bash
docker compose logs -f api
```

Follow database logs:

```bash
docker compose logs -f db
```

## Stop the stack

Stop and remove the containers and network while keeping the database volume:

```bash
docker compose down
```

Remove the containers, network, **and database volume**:

```bash
docker compose down -v
```

> Warning: `docker compose down -v` deletes the PostgreSQL data stored in `pgdata`.

## Key DevOps concepts demonstrated

- Docker image creation with a Dockerfile
- Layer ordering and build caching
- Python dependency installation
- Non-root containers
- Docker Compose service orchestration
- Container networking and service-name DNS
- Environment-based configuration
- PostgreSQL health checks
- `depends_on` with service health conditions
- Named volumes and persistent application data
- Port publishing
- Container logs and operational verification
