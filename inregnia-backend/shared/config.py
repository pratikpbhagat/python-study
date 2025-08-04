# shared/config.py
import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


def load_environment():
    env = os.getenv("APP_ENV", "local")
    root_dir = Path(__file__).resolve().parents[1]  # adjust to find the root folder
    env_path = root_dir / f".env.{env}"

    print(f"[DEBUG] Looking for .env at: {env_path}")
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        print(f"[DEBUG] Loaded .env from: {env_path}")
        print(f"[DEBUG] DYNAMODB_ENDPOINT: {os.getenv('DYNAMODB_ENDPOINT')}")
    else:
        raise FileNotFoundError(f"[ERROR] Env file not found: {env_path}")


# Load the env before anything else
load_environment()


class AppConfig(BaseSettings):
    # Dynamically load based on APP_ENV
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / f".env.{os.getenv('APP_ENV', 'local')}",
        env_file_encoding='utf-8'
    )

    app_env: str
    log_level: str
    dynamodb_region: str
    dynamodb_table_name: str
    dynamodb_endpoint: str
    cognito_domain: str
    cognito_client_id: str
    cognito_client_secret: str
    cognito_redirect_uri: str
    cognito_frontend_url: str
    cognito_identity_provider: str
    cognito_logout_redirect_uri: str

    @property
    def cognito_logout_url(self):
        return (
            f"{self.cognito_domain}/logout"
            f"?client_id={self.cognito_client_id}"
            f"&logout_uri={self.cognito_logout_redirect_uri}"
        )


# Singleton instance for usage in app
settings = AppConfig()
