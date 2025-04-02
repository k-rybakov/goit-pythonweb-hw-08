class Config:
    DB_URL = "postgresql+asyncpg://postgres:mysecretpassword@localhost:5432/contacts"
    JWT_SECRET = "secret"  # Секретний ключ для токенів
    JWT_ALGORITHM = "HS256"  # Алгоритм шифрування токенів
    JWT_EXPIRATION_SECONDS = 3600  # Час дії токена (1 година)


config = Config
