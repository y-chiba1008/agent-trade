from functools import lru_cache

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=('.env', '../.env'),
        env_file_encoding='utf-8',
        extra='ignore',
    )

    database_url: str | None = None

    @computed_field  # type: ignore[prop-decorator]
    @property
    def resolved_database_url(self) -> str:
        # DATABASE_URLが未設定の場合はエラーを出して即時停止
        if not self.database_url:
            raise RuntimeError(
                '環境変数 DATABASE_URL が設定されていません。サーバを起動できません。'
            )
        return self.database_url


@lru_cache
def get_settings() -> Settings:
    return Settings()


def validate_startup_settings() -> None:
    """起動に必要な環境変数を検証する。未設定なら RuntimeError。"""
    get_settings().resolved_database_url
