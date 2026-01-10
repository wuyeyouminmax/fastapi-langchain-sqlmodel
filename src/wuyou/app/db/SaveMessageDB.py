from sqlalchemy.ext.asyncio import AsyncSession

from wuyou.config.DBConfig import async_session
from wuyou.domain.po.SaveMessage import SaveMessage


class SaveMessageDB:
    def __init__(self,session: AsyncSession):
        self.session = session

    async def __aenter__(self):
        # 创建并启动一个异步数据库会话
        # 1. 创建一个新的数据库会话实例
        # 2. 调用会话的__aenter__方法进行初始化
        # 3. 返回一个SaveMessageDB实例，该实例会使用这个会话来操作数据库
        self.session = async_session()
        await self.session.__aenter__()
        return SaveMessageDB(self.session)
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # 退出异步上下文时自动调用
        # 1. 处理会话的清理工作
        # 2. 如果发生异常，异常信息会通过参数传递
        # 3. 自动调用会话的__aexit__方法，处理事务提交或回滚
        # 4. 确保会话被正确关闭，释放数据库连接
        await self.session.__aexit__(exc_type, exc_val, exc_tb)

    async def save(self,save_message: SaveMessage):
        # 增
        self.session.add(save_message)
        # 手动提交事务   推荐这种
        await self.session.commit()

# 工厂函数适用于用fastapi的depend
# 只适合fastapi依赖注入系统
async def create_save_message_db():
    async with async_session() as session:
        # yield这个表示是油管生成器函数，使用的async with上文管理器去管理绘画
        yield SaveMessageDB(session)

# 普通的函数也可以使用的，返回的是SaveMessageDB的实例
async def create_save_message_db_by_load():
    async with async_session() as session:
        return SaveMessageDB(session)