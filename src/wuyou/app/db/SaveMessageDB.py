from sqlalchemy.ext.asyncio import AsyncSession

from wuyou.config.DBConfig import async_session
from wuyou.domain.po.SaveMessage import SaveMessage


class SaveMessageDB:
    def __init__(self,session: AsyncSession):
        self.session = session

    async def save(self,save_message: SaveMessage):
        self.session.add(save_message)
        # 手动提交事务   推荐这种
        await self.session.commit()

# 工厂函数适用于用fastapi的depend
# 只适合fastapi依赖注入系统
async def create_save_message_db():
    async with async_session() as session:
        # yield这个表示是油管生成器函数，使用的async with上文管理器去管理绘画
        yield SaveMessageDB(session)
