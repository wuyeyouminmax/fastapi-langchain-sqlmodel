from fastapi import APIRouter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableBranch, RunnableLambda, RunnableParallel, RunnableSequence
from langchain_ollama import OllamaLLM
from loguru import logger

chainRouter = APIRouter()


@chainRouter.post("/demo1")
async def demo1():
    """一般调用"""
    """
    langchain的管道符 | 
        它是用来链接的
    """
    logger.info("进入了demo1")
    llm = OllamaLLM(
        model="qwen3:8b",
        reasoning=True  # 这个是关闭思考模型的回复
    )

    messages = [
        ("system", "你是一个小助手，告诉关于{topic}的笑话"),
        ("human", "告诉我关于的{jokeCount}个笑话"),
    ]

    prompt_template = ChatPromptTemplate.from_messages(messages)
    chain = prompt_template | llm | StrOutputParser()
    chain = prompt_template | llm
    result = await chain.ainvoke({"topic": "厨师", "jokeCount": 2})
    logger.info("==================")
    logger.info(result)
    return result

@chainRouter.post("/demo2")
async def demo2():
    model = OllamaLLM(
        model="qwen3:8b",
        reasoning=True  # 这个是关闭思考模型的回复
    )
    """判断"""
    # 5.分支---积极的提示词
    positive_feedback_template = ChatPromptTemplate.from_messages(
        [
            ("system", "你是一个非常有用的助手"),
            ("human", "为这个反馈生成积极的感谢信:{feedback}"),
        ]
    )
    # 5.分支---消极的提示词
    negative_feedback_template = ChatPromptTemplate.from_messages(
        [
            ("system", "你是一个非常有用的助手"),
            ("human", "为这个反馈生成负面的感谢信:{feedback}"),
        ]
    )
    # 5.分支---中立的提示词
    neutral_feedback_template = ChatPromptTemplate.from_messages(
        [
            ("system", "你是一个非常有用的助手"),
            ("human", "生成请求，了解此中立反馈的更多详细信息:{feedback}"),
        ]
    )
    # 5.分支---兜底，上报人工的
    escalate_feedback_template = ChatPromptTemplate.from_messages(
        [
            ("system", "你是一个非常有用的助手"),
            ("human", "生成一条消息以将此反馈上报给人工代理:{feedback}"),
        ]
    )
    # 3.判断情绪是哪一个
    classification_template = ChatPromptTemplate.from_messages(
        [
            ("system", "你是一个非常有用的助手"),
            ("human", "将此反馈的情绪生成为positive、negative、neutral、escalate:{feedback}"),
        ]
    )
    # 4.分支的判断
    # if x=positive
    # elif x=negative
    # elif x=neutral
    # else
    branches = RunnableBranch(
        (
            lambda x: "positive" in x,
            positive_feedback_template | model | StrOutputParser()
        ),
        (
            lambda x: "negative" in x,
            negative_feedback_template | model | StrOutputParser()
        ),
        (
            lambda x: "neutral" in x,
            neutral_feedback_template | model | StrOutputParser()
        ),
        escalate_feedback_template | model | StrOutputParser()
    )
    # 生成判断
    # classification_chain = classification_template | model | StrOutputParser()
    # # 判断进入那个分支中 | 进入分支
    # chain = classification_chain | branches
    # 等同于上面那两行代码
    chain = classification_template | model | StrOutputParser() | RunnableBranch(
        # RunnableBranch = if / elif / else
        (
            lambda x: "positive" in x,
            positive_feedback_template | model | StrOutputParser()
        ),
        (
            lambda x: "negative" in x,
            negative_feedback_template | model | StrOutputParser()
        ),
        (
            lambda x: "neutral" in x,
            neutral_feedback_template | model | StrOutputParser()
        ),
        escalate_feedback_template | model | StrOutputParser()
    )
    # 1.这个是传入的数据
    review = "该产品非常出色。我真的很喜欢使用它，并发现它非常有用。"
    # 2.入口
    result = chain.invoke({"feedback": review})
    # 6.返回结果
    return result

@chainRouter.post("/demo3")
async def demo3():
    """针对上面langchain链式调用的扩展,针对输出结果，进行定式输出"""
    model = OllamaLLM(
        model="qwen3:8b",
        reasoning=True  # 这个是关闭思考模型的回复
    )
    messages = [
        ("system", "你是一个喜剧演员，告诉关于{topic}的笑话"),
        ("human", "告诉我关于的{jokeCount}个笑话"),
    ]
    promptTemplate = ChatPromptTemplate.from_messages(messages)
    countWord = RunnableLambda(lambda x: f"共计:{len(x)}==============\n\n\n\n\n\n\\n{x}")
    chain = promptTemplate | model | StrOutputParser()  | countWord
    response = chain.invoke({"topic": "律师", "jokeCount": 3})
    return response

@chainRouter.post("/demo4")
async def demo4():
    """langchain的并发"""
    model = OllamaLLM(
        model="qwen3:8b",
        reasoning=True  # 这个是关闭思考模型的回复
    )
    # 列出产的特点，在执行并发前
    messages = [
        ("system", "你是产品分析专家"),
        ("human", "需要您列出{productName}的主要功能"),
    ]
    promptTemplate = ChatPromptTemplate.from_messages(messages)
    # 并发分析前景和缺点
    def analyzePros(features):
        prosTemplate = ChatPromptTemplate.from_messages(
            [
                ("system", "你是一个专家产品审评"),
                ("human", "考虑这些特性:{features}, 列出改特性的前景"),
            ]
        )
        return prosTemplate.format_prompt(features=features)

    def analyzeCons(features):
        crosTemplate = ChatPromptTemplate.from_messages(
            [
                ("system", "你是一个专家产品审评"),
                ("human", "考虑这些特性:{features}, 列出这些特性的缺点"),
            ]
        )
        return crosTemplate.format_prompt(features=features)

    def combineProCons(pros, cons):
        return f"前景:\n{pros}\n\nCons:\n{cons}"

    prosBranchChain = (
            RunnableLambda(lambda x: analyzePros(x)) | model | StrOutputParser()
    )
    consBranchChain = (
            RunnableLambda(lambda x: analyzeCons(x)) | model | StrOutputParser()
    )
    # 2.执行的流程
    chain = (
            promptTemplate # 提示词
            | model # llm 进行推理
            | StrOutputParser() # 直接返回内容,不需要元数据
            # 2.1 执行并发
            | RunnableParallel(branches={"pros": prosBranchChain, "cons": consBranchChain})
            | RunnableLambda(
        lambda x: print("最终输出", x) or combineProCons(x["branches"]["pros"], x["branches"]["cons"]))
    )
    # 1.输入的数据
    result = chain.invoke({"productName": "linux操作系统"})
    print(result)
    return result

@chainRouter.post("/demo5")
async def demo5():
    """
    使用 LangChain 的 RunnableSequence 构建一个链式调用示例。
    这个函数展示了如何将多个处理步骤按顺序组合成一个可执行的链。
    """
    # 1. 初始化 Ollama 语言模型
    # - 使用 qwen3:8b 模型
    # - reasoning=True 表示关闭思考模型的回复
    model = OllamaLLM(
        model="qwen3:8b",
        reasoning=True
    )
    # 2. 定义对话模板
    # - system 消息设置 AI 的角色
    # - human 消息定义用户输入模板
    messages = [
        ("system", "你是一个喜剧演员，告诉关于{topic}的笑话."),
        ("human", "告诉我关于的{jokeCount}个笑话."),
    ]
    # 3. 创建提示词模板
    promptTemplate = ChatPromptTemplate.from_messages(messages)
    # 4. 定义处理步骤
    # 4.1 格式化提示词：将输入参数应用到模板
    formatPrompt = RunnableLambda(lambda x: promptTemplate.format(**x))
    # 4.2 调用模型：将格式化后的提示词发送给模型
    invokeModel = RunnableLambda(lambda x: model.invoke(x))

    # 4.3 解析输出：这里直接返回原始输出
    parseOutput = RunnableLambda(lambda x: x)

    # 5. 构建处理链
    # - first: 第一个处理步骤（格式化提示词）
    # - middle: 中间处理步骤列表（调用模型）
    # - last: 最后一个处理步骤（解析输出）
    chain = RunnableSequence(
        first=formatPrompt,
        middle=[invokeModel],
        last=parseOutput
    )
    # 6. 调用处理链并返回结果
    # 输入参数：主题为"律师"，请求3个笑话
    response = chain.invoke({"topic": "律师", "jokeCount": 3})
    return response