from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "FAST_API Application"
    API_V1_STR: str = "/api/v1"



    # Database settings
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    SMTP_PORT: int = 587
    SMTP_SERVER: str = "smtp.gmail.com"
    SENDER_EMAIL: str
    GMAIL_APP_PASS: str
    DROP_TABLES_ON_STARTUP: bool = False
    # Security settings
    SECRET_KEY: str
    EMAIL_VERIFICATION_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
