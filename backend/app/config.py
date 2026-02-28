from pydantic import BaseModel
import os


class Settings(BaseModel):
    environment: str = os.getenv("ENVIRONMENT", "local")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./data.db")
    artifacts_repo_path: str = os.getenv("ARTIFACTS_REPO_PATH", "~/local/code/werii-gather")
    artifacts_git_auto_push: bool = os.getenv("ARTIFACTS_GIT_AUTO_PUSH", "false").lower() == "true"
    github_token: str = os.getenv("GITHUB_TOKEN", "")
    github_repo: str = os.getenv("GITHUB_REPO", "")
    llm_provider: str = os.getenv("LLM_PROVIDER", "openai")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    google_docs_enabled: bool = os.getenv("GOOGLE_DOCS_ENABLED", "false").lower() == "true"
    google_credentials_json: str = os.getenv("GOOGLE_CREDENTIALS_JSON", "")
    daily_timezone: str = os.getenv("DAILY_TIMEZONE", "America/Chicago")
    daily_hour: int = int(os.getenv("DAILY_HOUR", "2"))
    daily_minute: int = int(os.getenv("DAILY_MINUTE", "0"))
    write_api_token: str = os.getenv("WRITE_API_TOKEN", "")
    max_upload_bytes: int = int(os.getenv("MAX_UPLOAD_BYTES", "10485760"))


settings = Settings()
