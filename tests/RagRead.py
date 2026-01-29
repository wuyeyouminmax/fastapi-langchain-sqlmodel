import chromadb
from langchain_ollama import OllamaEmbeddings

llm = OllamaEmbeddings(model="bge-m3")
query_text = "云韵在魔兽山脉跟什么人打架？"

query_embedding = llm.embed_query(query_text)
client = chromadb.PersistentClient(path=r"D:\Code\teach\wuyou\tests\db")

collection_name = "doupo"
collection = client.get_collection(collection_name)
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3,

)
print(results)
print("完成")