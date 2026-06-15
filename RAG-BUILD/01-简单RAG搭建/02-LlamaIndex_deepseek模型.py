import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# 1. 配置API
SILICONFLOW_API_BASE = "https://api.siliconflow.cn/v1/"
SILICONFLOW_API_KEY = "sk-veznsdtqgjdltmwmxzpjlbvzutkikczwgpkroayiuwvetuon"

# LLM配置
Settings.llm = OpenAI(
    api_key=SILICONFLOW_API_KEY,
    api_base=SILICONFLOW_API_BASE,
    model="Qwen/Qwen3-VL-32B-Thinking",
    temperature=0.7
)

# Embedding配置（使用合法模型名绕过验证）
Settings.embed_model = OpenAIEmbedding(
    api_key=SILICONFLOW_API_KEY,
    api_base=SILICONFLOW_API_BASE,
    model="Qwen/Qwen3-Embedding-0.6B"  # 硅基流动会映射到对应模型
)

# 2. 加载文档（关键：使用../）
try:
    print("正在加载文档...")
    file_path = "D:\Desktop\AI-treasure_trove\RAG-BUILD\90-文档-Data\黑悟空\黑悟空wiki.txt"
    
    # 验证路径
    if os.path.exists(file_path):
        print(f"✓ 找到文件: {os.path.abspath(file_path)}")
        documents = SimpleDirectoryReader(input_files=[file_path]).load_data()
        print(f"✓ 成功加载 {len(documents)} 个文档")
    else:
        print(f"✗ 文件不存在: {file_path}")
        print(f"当前目录: {os.getcwd()}")
        print(f"尝试的绝对路径: {os.path.abspath(file_path)}")
        exit()
        
except Exception as e:
    print(f"加载失败: {e}")
    exit()

# 3. 构建索引
print("构建向量索引...")
index = VectorStoreIndex.from_documents(documents)
print("索引构建完成")

# 4. 查询
query_engine = index.as_query_engine()
question = "黑神话悟空中有哪些战斗工具?"
print(f"\n问题: {question}")

response = query_engine.query(question)
print(f"回答: {response}")