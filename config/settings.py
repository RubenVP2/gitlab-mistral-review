from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    gitlab_token: str = Field(..., env="GITLAB_TOKEN")
    gitlab_url: str = Field(default="https://gitlab.com/api/v4", env="GITLAB_URL")
    mistral_key: str = Field(..., env="MISTRAL_API_KEY")

    cache_file: str = Field(default="cache.json", env="CACHE_FILE")
    polling_interval: int = Field(default=300, env="POLLING_INTERVAL")
    max_tokens: int = Field(default=8000, env="MAX_TOKENS")

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
