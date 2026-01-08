from fastapi import APIRouter
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from src.wuyou.domain.AiMessages import MessageA
from langchain_ollama import OllamaLLM
messageRouter = APIRouter()

@messageRouter.post("/demo1")
async def demo1():
    return "测试子路由"

@messageRouter.post("/demo2")
async def demo2(data:MessageA):
    print(f"data={data}")
    return "参数校验"

@messageRouter.post("/demo3")
async def demo3(data:str):
    llm = OllamaLLM(
        model="qwen3:8b",
        reasoning=True  # 这个是关闭思考模型的回复
    )
    # llm.invoke() 普通函数
    # await llm.ainvoke() 异步函数，必须要要加await
    # 在python中 异步函数可以调用普通的函数，但普通函数无法调用异步函数
    message_list = [SystemMessage("你是wuyou的女朋友"),
                    HumanMessage("你是谁?"),
                    AIMessage("*轻轻靠在你肩上* 你终于来啦~我叫小雨，是wuyou的女朋友哦。今天他忙完工作回来，我就给他做了他最爱吃的红烧肉，你来得正好，要不要一起吃晚饭？我刚把菜热好啦~"),
                    HumanMessage(data)]
    res = await llm.ainvoke(message_list)
    return res