"""Typed configuration models for the ETL pipeline, loaded from config.yaml."""

from pathlib import Path

from pydantic import Field, BaseModel, field_validator
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict
from pydantic_settings.sources import YamlConfigSettingsSource

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent.parent
CONFIG_FILE = BASE_DIR / "config.yaml"

class HeaderSettings(BaseModel):
    """HTTP headers sent with NSE archive requests, aliased to match config.yaml's casing."""
    model_config = SettingsConfigDict(populate_by_name=True)

    user_agent: str = Field(alias="User-Agent")
    accept: str = Field(alias="Accept")
    accept_language: str = Field(alias="Accept-Language")
    accept_encoding: str = Field(alias="Accept-Encoding")
    referer: str = Field(alias="Referer")

class RetrySettings(BaseModel):
    """tenacity retry parameters for bhavcopy download attempts."""
    stop_after_attempts: int
    wait_multiplier: float
    wait_min: float
    wait_max: float

class RateLimitSettings(BaseModel):
    """Request throttling parameters enforced via pyrate_limiter."""
    max_requests: int
    duration_milliseconds: int

class NSEClientConfig(BaseSettings):
    """Configurations for NSEClient"""
    model_config = SettingsConfigDict(
        yaml_file=CONFIG_FILE,
        yaml_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    download_dir: Path
    archive_url: str
    connection_timeout: float
    headers: HeaderSettings
    retry: RetrySettings
    rate_limit: RateLimitSettings

    @field_validator("download_dir")
    @classmethod
    def resolve_and_create_download_dir(cls, v: Path) -> Path:
        """Resolves download_dir relative to the project root (if not already absolute) and ensures it exists."""
        resolved = v if v.is_absolute() else PROJECT_ROOT / v
        resolved.mkdir(parents=True, exist_ok=True)
        return resolved

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            YamlConfigSettingsSource(settings_cls),
        )

class ExtractorConfig(BaseSettings):
    """Configurations for Extractor"""
    model_config = SettingsConfigDict(
        yaml_file=CONFIG_FILE,
        yaml_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    extract_dir: Path

    @field_validator("extract_dir")
    @classmethod
    def resolve_and_create_download_dir(cls, v: Path) -> Path:
        """Resolves extract_dir relative to the project root (if not already absolute) and ensures it exists."""
        resolved = v if v.is_absolute() else PROJECT_ROOT / v
        resolved.mkdir(parents=True, exist_ok=True)
        return resolved

    @classmethod
    def settings_customise_sources(
            cls,
            settings_cls: type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            YamlConfigSettingsSource(settings_cls),
        )

class DBConfig(BaseSettings):
    model_config = SettingsConfigDict(
        yaml_file=CONFIG_FILE,
        yaml_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    db_path: Path

    @field_validator("db_path")
    @classmethod
    def resolve_and_create_db_path(cls, v: Path) -> Path:
        resolved = v if v.is_absolute() else PROJECT_ROOT / v
        resolved.parent.mkdir(parents=True, exist_ok=True)
        return resolved

    @classmethod
    def settings_customise_sources(
            cls,
            settings_cls: type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            YamlConfigSettingsSource(settings_cls),
        )


client_config = NSEClientConfig()
extractor_config = ExtractorConfig()
db_config = DBConfig()