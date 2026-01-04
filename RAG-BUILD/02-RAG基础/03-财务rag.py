from chromadb import Settings
from dotenv import load_dotenv
from openai import OpenAI
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
import chromadb
import os

# 按照固定字符切割文档
def sliding_window_chunks(text, chunk_size, stride):
    return [text[i:i + chunk_size] for i in range(0, len(text), stride)]

# 读取PDF
def extract_text_from_pdf(filename, page_numbers=None):
    '''从 PDF 文件中（按指定页码）提取文字'''
    full_text = ''
    # 提取全部文本
    for i, page_layout in enumerate(extract_pages(filename)):
        # 如果指定了页码范围，跳过范围外的页
        if page_numbers is not None and i not in page_numbers:
            continue
        for element in page_layout:
            # 检查element是不是文本
            if isinstance(element, LTTextContainer):
                # print(element.get_text())
                # 将换行和空格去掉
                full_text += element.get_text().replace("\n", "").replace(" ", "")

    text_chunks = sliding_window_chunks(full_text, 250, 100)

    return text_chunks

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

    def get_embeddings(self,texts,model="text-embedding-v2"):
        '''封装 qwen 的Embedding 模型接口'''
        data = client.embeddings.create(input=texts,model=model).data
        return [x.embedding for x in data]

    def add_documents(self,documents):
        '''向collection中添加文档与向量'''

        # 将数据向量化
        embeddings = self.get_embeddings(documents)

#         将向量化的数据和原文存入向量数据库
        self.collection.add(
            embeddings=embeddings,    # 每个文档的向量
            documents = documents,      # 文档的原文
            ids=[f"id{i}" for i in range(len(documents))]  # 文档的每个id
        )

    def search(self, query,top_n):
        '''检索向量数据库'''
        # 把我们查询的问题向量化, 在chroma当中进行查询
        # D:\software\miniconda\envs\py_ai\Lib\site-packages\chromadb\segment\impl\vector\local_hnsw.py  默认相似度匹配欧式距离
        results = self.collection.query(
            query_embeddings=self.get_embeddings([query]),
            n_results=top_n,   # topK
        )
        return results

class RAG_Bot:
    def __init__(self, vector_db, n_results=2):
        self.vector_db = vector_db
        self.n_results = n_results

    # llm模型
    def get_completion(self, prompt, model="qwen-plus"):
        '''封装 千问 接口'''
        messages = [{"role": "user", "content": prompt}]
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0,  # 模型输出的随机性，0 表示随机性最小
        )
        # print(response)
        return response.choices[0].message.content

    def chat(self, user_query):
        # 1. 检索
        search_results = self.vector_db.search(user_query, self.n_results)
        print('search_results:', search_results)
        # 2. 构建 Prompt
        prompt = prompt_template.replace("__INFO__", "\n".join(search_results['documents'][0])).replace("__QUERY__",
                                                                                                        user_query)
        print('prompt:', prompt)
        # 3. 调用 LLM
        response = self.get_completion(prompt)
        return response

if __name__ == '__main__':
    load_dotenv()
    client = OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"),
                    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
    prompt_template = """                                             """
    docx_file = './data_file/财务管理文档.pdf'
    # 读取pdf文件
    # paragraphs = extract_text_from_docx(docx_filename, min_line_length=10)
    paragraphs = extract_text_from_pdf(docx_file, page_numbers=[0, 1, 2])
    # print(paragraphs)
    vector_db = MyVectorDBConnector("demo")
    # 向向量数据库中添加文档
    vector_db.add_documents(paragraphs)

    # 创建一个RAG机器人
    bot = RAG_Bot(
        vector_db
    )
    user_query = "财务管理权限划分?"
    response = bot.chat(user_query)
    print(response)