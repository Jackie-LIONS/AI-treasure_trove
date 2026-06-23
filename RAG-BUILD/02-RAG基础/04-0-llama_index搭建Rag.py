import os
from llama_index.core import PromptTemplate, Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms.dashscope import DashScope
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from dotenv import load_dotenv
load_dotenv()

Settings.llm = DashScope(
    model="qwen-plus",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    api_base=os.getenv("DASHSCOPE_API_BASE")
)
Settings.embed_model = HuggingFaceEmbedding(
    model_name=r"D:\LLM\Local_model\BAAI\bge-large-zh-v1___5",
    device="cuda",  # 指定使用显卡来跑，也可选：cpu
)

qa_prompt_str = """你是一个有帮助的AI助手。请根据下面提供的上下文信息，准确、简洁地回答用户的问题。
如果上下文无法回答问题，请直接说“我不知道”或“上下文没有相关信息”，不要编造答案。

上下文信息如下:
{context_str}

用户问题: {query_str}
请用中文回答：
"""
qa_prompt = PromptTemplate(qa_prompt_str)

documents = SimpleDirectoryReader(
    input_files=['./data_file/deepseek介绍.txt']  # 可选：限制文件类型
).load_data()

print(f"加载了 {len(documents)} 个文档")

# 构建向量索引（会自动chunk + embedding）
index = VectorStoreIndex.from_documents(
    documents,
    show_progress=True
)

# 创建 Query Engine，并使用自定义提示词
query_engine = index.as_query_engine(
    similarity_top_k = 5,               # 检索前5个最相关片段
    text_qa_template = qa_prompt,       # 使用自定义提示词
    streaming=False                     # 如果想流式输出可设为True
)

question = 'deepseek什么时候遭到攻击?'
response = query_engine.query(question)
print("\n回答：")
print(response.response)

# 如果想看检索到的上下文来源：
print("\n--- 来源节点 ---")
for node in response.source_nodes:
    print(f"相似度: {node.score:.4f} | 文件: {node.metadata.get('file_name')}")

