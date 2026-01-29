import chromadb
from langchain_community.document_loaders import TextLoader
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. 加载文本文件
loader = TextLoader(
    r"D:\Code\teach\wuyou\tests\斗破苍穹.txt",
    encoding="utf-8"
)
documents = loader.load()

# 2. 递归字符切割器（推荐）
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=612,# 一个块的大小
    chunk_overlap=100, # 回文
    separators=[
        "\n\n",
        "\n",
        "。", "！", "？", "；",
        ".", "!", "?", ";",
        "，", ",",
        "：", ":",
        " ",
        ""
    ],# 分隔符
)
# 3. 执行切割
docs = text_splitter.split_documents(documents)
# 切割完了下一步是进行向量化

# 4.引入向量模型
embedding_model = OllamaEmbeddings(model="bge-m3")

# 5.进行向量化
docs_list = []
i = 0
for item in docs:
    docs_list.append(item.page_content)
    if i > 2000:
        break
    i += 1

# embeddings = embedding_model.embed_query(docs[100].page_content)
embedding_list = embedding_model.embed_documents(docs_list)

# 6.存储到chromadb中
client = chromadb.PersistentClient(
    path=r"D:\Code\teach\wuyou\tests\db"
)

collection_name = "doupo"

collection = client.get_or_create_collection(
    name=collection_name
)
ids = [f"doc_{i}" for i in range(len(docs_list))]

# 6️⃣ 一次性写入
collection.add(
    documents=docs_list,
    embeddings=embedding_list,
    ids=ids,
)

print(f"原本块:{len(docs_list)}/{len(embedding_list)}")
# print(f"{docs[100].page_content}：{len(docs[100].page_content)}")
# print("=================================================================")
# print(f"维度是:{len(embeddings)}\n{embeddings}")
# print(f"{docs[101].page_content}")
# print("=================================================================")
# print(f"{docs[99].page_content}")
print(f"文本切割写入完成，共 {len(docs)} 个 chunk:{docs[i].page_content}")