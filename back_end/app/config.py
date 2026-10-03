from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./database.db"

    mail_username: str = ""
    mail_password: str = ""
    mail_from: str = "no-reply@example.com"
    mail_from_name: str = "Escola API"
    mail_port: int = 587
    mail_server: str = "smtp.gmail.com"
    mail_starttls: bool = True
    mail_ssl_tls: bool = False
    portal_url: str = "http://localhost:5173"

    whatsapp_default_country_code: str = "55"


settings = Settings()
