import uvicorn
from loguru import logger
from wuyou.config.Settings import settings
# 配置日志文件
logger.add(
    settings.LOG_PATH,
    rotation="500 MB",      # 单文件最大大小
    encoding="utf-8",
    compression="zip",      # 历史日志压缩
    enqueue=True,           # 多进程安全
    level="INFO"
)
if __name__ == '__main__':
    uvicorn.run("app:app",host=settings.HOST,port=settings.PORT,reload=True)