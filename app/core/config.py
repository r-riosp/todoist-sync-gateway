from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    app_name: str = "Todoist Gateway to AnyType and Linear"
    app_description: str = "Gateway that syncs tasks from Todoist to AnyType and Linear"
    app_version: str = "0.1.0"
    debug: bool = True
    db_user: str = ""
    db_password: str = ""
    db_name: str = ""

    # External API Keys and URLs
    todoist_api_key: str
    anytype_api_key: str
    anytype_base_url: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
config = Config()
