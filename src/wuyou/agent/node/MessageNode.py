from wuyou.app.db.SaveMessageDB import create_save_message_db_by_load
from wuyou.domain.po.SaveMessage import SaveMessage


class MessageNode:
    def __init__(self,save_message_db):
        self.save_message_db = save_message_db

    @classmethod
    async def create(cls):
        save_message_db = await create_save_message_db_by_load()
        return cls(save_message_db)

    async def demo_node(self):
        await self.save_message_db.save(SaveMessage(type="test",content="test"))