# Hometask FastAPI

**Run PSQL docker container:**

```bash
docker run --name postgres-contacts -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres
```

**Create new database**:

```bash
docker exec -it postgres-contacts psql -U postgres -c "CREATE DATABASE contacts;"
```

**Run migrations**:

```bash
alembic upgrade head
```

**Run project**:

```bash
uvicorn main:app --reload
```

**Swagger documentation**:
http://127.0.0.1:8000/docs
