import chromadb
from chromadb.config import Settings
import json
from openai import OpenAI
from dotenv import load_dotenv
import os

class MyVectorDBConnector:
    def __init__(self,collection_name):
#         创建chroma数据库连接
        chroma_client = chromadb.Client(Settings(allow_reset=True))

        # 创建一个 collection
        # cosine余弦相似度  默认欧式距离
        self.collection = chroma_client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def get_embeddings(self,texts,model="text-embedding-v3"):
        '''封装 qwen 的Embedding 模型接口'''
        data = chromadb_client.embeddings.create(input=texts,model=model).data
        return [x.embedding for x in data]

    def add_documents(self,instructions,outputs):
        '''向collection中添加文档与向量'''

        # 将数据向量化
        embeddings = self.get_embeddings(instructions)

#         将向量化的数据和原文存入向量数据库
        self.collection.add(
            embeddings=embeddings,    # 每个文档的向量
            documents = outputs,      # 文档的原文
            ids=[f"id{i}" for i in range(len(outputs))]  # 文档的每个id
        )

    def search(self, query):
        '''检索向量数据库'''
        # 把我们查询的问题向量化, 在chroma当中进行查询
        # D:\software\miniconda\envs\py_ai\Lib\site-packages\chromadb\segment\impl\vector\local_hnsw.py  默认相似度匹配欧式距离
        results = self.collection.query(
            query_embeddings=self.get_embeddings([query]),
            n_results=2,   # topK
        )
        return results


if __name__ == '__main__':
    load_dotenv()
    chromadb_client = OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"), base_url=os.getenv("DASHSCOPE_BASE_URL"))
    # 读取文件
    with open('./data_file/train_zh.json', 'r', encoding='utf-8') as f:
        data = [json.loads(line) for line in f]
    # print(data)
    # print(data[0:100])

    # 获取前10条的问题和输出
    instructions = [entry['instruction'] for entry in data[0:10]]
    outputs = [entry['output'] for entry in data[0:10]]
    # print(instructions)
    # print("-------------------------------------------------")
    # print(outputs)

    vector_db = MyVectorDBConnector("demo")
    vector_db.add_documents(instructions,outputs)
    user_query = "得了白癜风怎么办？"
    results = vector_db.search(user_query)
    print(results)

