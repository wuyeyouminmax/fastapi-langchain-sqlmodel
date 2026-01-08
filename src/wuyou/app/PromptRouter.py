from fastapi import APIRouter
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from loguru import logger
promptRouter = APIRouter()
### 重点:在langchain的三种消息中不支持占位符的
@promptRouter.post("/demo1")
async def demo1():
    # 将字符串转化成提示词模板
    template = "跟我说{count}个笑话"
    prompt_template = ChatPromptTemplate.from_template(template)
    res = prompt_template.invoke({"count":3})
    # 后面就是rag中切割成chunk里面，需要根据chunk所属的内容以及大小去提取出问题，方便微调，
    # 根据上述的内容提出去{count}个问题出来
    return res
@promptRouter.post("/demo2")
async def demo2():
    # 将字符串转化成提示词模板---有多个占位符
    template = "跟我说{count}个关于{kind}笑话"
    prompt_template = ChatPromptTemplate.from_template(template)
    res = prompt_template.invoke({"count":3,"kind":"厨师"})
    # 后面就是rag中切割成chunk里面，需要根据chunk所属的内容以及大小去提取出问题，方便微调，
    # 根据上述的内容提出去{count}个问题出来
    return res
@promptRouter.post("/demo3")
async def demo3():
    # 将字符串转化成提示词模板---在langchain的三种消息中不支持这种模板转化
    message = [
        ("system","你是一个专业的讲笑话的人，喜欢讲{kind}这个笑话"),
        HumanMessage("请你讲{count}个笑话")
    ]
    prompt_template = ChatPromptTemplate.from_messages(message)
    res = prompt_template.invoke({"count": 3, "kind": "厨师"})

    return res
@promptRouter.post("/demo4")
async def demo4(count:int):
    # 将字符串转化成提示词模板
    template = "跟我说{count}个笑话"
    prompt_template = ChatPromptTemplate.from_template(template)
    prompt = prompt_template.invoke({"count":count})
    llm = OllamaLLM(
        model="qwen3:8b",
        reasoning=True  # 这个是关闭思考模型的回复
    )
    res = await llm.ainvoke(prompt)
    return res
@promptRouter.post("/demo5")
async def demo5(count:int,kind:str):
    # 将字符串转化成提示词模板---有多个占位符
    template = "跟我说{count}个关于{kind}笑话"
    prompt_template = ChatPromptTemplate.from_template(template)
    prompt = prompt_template.invoke({"count":count,"kind":kind})
    logger.info(f"本次的提示词模板:\n{prompt}")
    llm = OllamaLLM(
        model="qwen3:8b",
        reasoning=True  # 这个是关闭思考模型的回复
    )
    res = await llm.ainvoke(prompt)
    return res
@promptRouter.post("/demo6")
async def demo6(count:int,kind:str):
    logger.info(f"参数count={count},kind={kind}")
    # 将字符串转化成提示词模板---在langchain的三种消息中
    message = [
        SystemMessage("你是一个专业的讲笑话的人，喜欢讲{kind}这个笑话"),
        HumanMessage("请你讲{count}个笑话")
    ]
    prompt_template = ChatPromptTemplate.from_messages(message)
    prompt = prompt_template.invoke({"count": count,"kind": kind})
    logger.info(f"本次的提示词模板:\n{prompt}")
    llm = OllamaLLM(
        model="qwen3:8b",
        reasoning=True  # 这个是关闭思考模型的回复
    )
    res = await llm.ainvoke(prompt)
    return res
@promptRouter.post("/demo7")
async def demo7(count:int,kind:str):
    logger.info(f"参数count={count},kind={kind}")
    # 将字符串转化成提示词模板---在langchain的三种消息中
    message = [
        ("system","你是一个专业的讲笑话的人，喜欢讲{kind}这个笑话"),
        ("user","请你讲{count}个笑话")
    ]
    prompt_template = ChatPromptTemplate.from_messages(message)
    prompt = prompt_template.invoke({"count": count,"kind": kind})
    logger.info(f"本次的提示词模板:\n{prompt}")
    llm = OllamaLLM(
        model="qwen3:8b",
        reasoning=True  # 这个是关闭思考模型的回复
    )
    res = await llm.ainvoke(prompt)
    return res