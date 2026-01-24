from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.params import Depends
from langchain_ollama import OllamaLLM
from loguru import logger

from wuyou.agent.node.MessageGraph import get_message_graph, MessageGraph
from wuyou.app.ChainRouter import chainRouter
from wuyou.app.MessageRouter import messageRouter
from wuyou.app.PromptRouter import promptRouter


# 生命周期管理器(启动和关闭时候会执行的)
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("项目启动")#在项目启动之前
    yield
    logger.info("关闭中")#在项目关闭之前
app = FastAPI(
    title="基础环境的搭建",
    version="1.0",
    deprecation="开始搭建自己的python基础服务",
    lifespan=lifespan,# 指定生命周期管理器
)
# 子路由
# 注册路由 chainRouter
app.include_router(messageRouter,prefix="/message",tags=["消息"])
app.include_router(promptRouter,prefix="/prompt",tags=["提示词模板"])
app.include_router(chainRouter,prefix="/chain",tags=["链式调用"])
# 测试
@app.get('/test')
async def test(message:str):
    llm = OllamaLLM(
        model="qwen3:8b",
        reasoning=True  # 这个是关闭思考模型的回复
    )
    res = llm.invoke(message)
    return res

@app.post('/demo1')
async def demo1(data:int,message_graph:MessageGraph=Depends(get_message_graph)):
    """
    用户输入一个数字
    让llm随机生成一个数字
    比较大小
    如果llm的数字大，发表获胜感谢
    如果llm的数字小，发表失败的感想
    :param data:
    :param message_graph:
    :return:
    """
    print(data)
    # 1.入口
    result = await message_graph.run_runnable(data)
    return result
