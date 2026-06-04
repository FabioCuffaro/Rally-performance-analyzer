"""Application configuration loaded from environment variables."""

from pathlib import Path
from pydantic_settings import BaseSettings  # pydantic v2


class Settings(BaseSettings):
    # API server
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True

    # Dashboard
    dashboard_api_url: str = "http://localhost:8000"

    # Paths (resolved relative to project root)
    data_raw_path: str = "data/raw"
    data_processed_path: str = "data/processed"

    @property
    def project_root(self) -> Path:
        """Absolute path to the project root (two levels up from this file)."""
        return Path(__file__).resolve().parents[2]

    @property
    def raw_dir(self) -> Path:
        return self.project_root / self.data_raw_path

    @property
    def processed_dir(self) -> Path:
        return self.project_root / self.data_processed_path

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
