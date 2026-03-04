from fastapi import Depends
from langchain_ollama import OllamaLLM

from wuyou.agent.node.MessageState import MessageState
from wuyou.app.db.SaveMessageDB import SaveMessageDB, create_save_message_db
from wuyou.domain.po.SaveMessage import SaveMessage


class MessageNode:
    def __init__(self,save_message_db:SaveMessageDB):
        self.save_message_db = save_message_db


    async def demo_node(self):
        await self.save_message_db.save(SaveMessage(type="test",content="test"))

    async def demo_crate_score(self,data:MessageState):
        print("1.llm生成一个分数")
        llm = OllamaLLM(
            model="qwen3:8b",
            reasoning=True  # 这个是关闭思考模型的回复
        )
        await self.save_message_db.save(SaveMessage(type="test", content="test"))
        result = await llm.ainvoke("请生成一个数字，要一到一百之内,要的是数字的:0-100")
        data.ai_data = int(60)
        return data

    async def demo_check(self,data:MessageState):
        print(f"2.进入判断节点:{data}")
        await self.save_message_db.save(SaveMessage(type="test", content="test"))
        if data.user_data <= data.ai_data:
            return "loser"
        else:
            return "winner"
    async def demo_winner(self,data:MessageState):
        print("3.1.发表胜利感谢")
        llm = OllamaLLM(
            model="qwen3:8b",
            reasoning=True  # 这个是关闭思考模型的回复
        )
        result = await llm.ainvoke("生成一个胜利的发表感")
        await self.save_message_db.save(SaveMessage(type="test", content="test"))
        data.message=result
        return data

    async def demo_loser(self,data:MessageState):
        print("3.2.发表失败感谢")
        llm = OllamaLLM(
            model="qwen3:8b",
            reasoning=True  # 这个是关闭思考模型的回复
        )
        result = await llm.ainvoke("生成一个失败的发表感")
        data.message = result
        return data
async def get_message_node(save_message_db: SaveMessageDB = Depends(create_save_message_db)) -> MessageNode:
    return MessageNode(save_message_db)

