from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "JWI Drive Intelligence API"

    clients_root_folder_id: str = "1-3FfMbvGrddiOHboFeNxUOAy6ds8uIFM"
    active_work_folder_name: str = "01. Working"

    google_client_id: str = ""
    google_client_secret: str = ""
    google_refresh_token: str = ""

    default_days: int = 45
    max_clients: int = 100
    max_projects_per_client: int = 100

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
