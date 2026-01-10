from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# 加载 .env 文件
load_dotenv()

class Settings(BaseSettings):
    """
    项目统一配置入口
    """
    DATABASE_PG_URL: str = Field(default="未定义")
    HOST: str = Field(default="127.0.0.1", description="服务监听地址")
    PORT: int = Field(default=8091, description="服务端口")
    LOG_PATH: str = Field(default="./logs/app.log", description="日志文件路径")
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

# 创建全局配置对象
settings = Settings()