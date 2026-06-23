from llama_index.llms.openai import OpenAI

# # 1. 调用国外的模型时，可以直接使用OpenAI() 这个类
# llm = OpenAI(model= 'gpt-4o-mini')
# response = llm.complete("你好")

# 2. 使用OpenAILike（是 OpenAI 模型的一个轻量级封装，使其能够与提供 OpenAI 兼容 API 的第三方工具兼容。）
#    可以调用所有的模型

#   2.1 加载在线模型
# import os
# from dotenv import load_dotenv
# from llama_index.llms.openai_like import OpenAILike
# load_dotenv()
#
# llm = OpenAILike(
#     model='qwen3.5-plus',
#     api_key=os.getenv("DASHSCOPE_API_KEY"),
#     api_base=os.getenv('DASHSCOPE_BASE_URL'),
#     is_chat_model=True,    # 是否是chat_model
# )
# response = llm.complete("hello")
# print(response)
#
# #  2.2 加载离线模型
# from llama_index.llms.openai_like import OpenAILike
#
# llm = OpenAILike(
#     model="qwen2.5:7b",
#     api_key='1111',   # 本地key可以随便填
#     api_base='http://localhost:11434/v1',
#     # is_chat_model=True,   # 是否是 Chat Model
# )
#
# response = llm.complete("你好")
# print(response)

# 3. 其它接口调用
# 3.1 各个厂商接口封装：给厂商封装的接口,相比较OpenAILike实现的功能会更加精细  pip install llama-index-llms-dashscope 后面的dashscope 是针对不同厂商的名称
# 接口地址:https://developers.llamaindex.ai/python/framework-api-reference/llms/
# 模型厂商都会开放sdk接口,LlamaIndex 团队基于这个官方 SDK，编写了适配层，
# 让 模型厂商 的 API 能无缝符合 LlamaIndex 的 LLM 抽象接口
# （支持 chat()、complete()、stream_chat()、工具调用、Function Calling 等）
# from llama_index.llms.dashscope import DashScope, DashScopeGenerationModels
# import os
# from dotenv import load_dotenv
# load_dotenv()
#
# llm = DashScope(
#     model_name=DashScopeGenerationModels.QWEN_PLUS,   # 选择模型
#     api_key=os.getenv("DASHSCOPE_API_KEY"),
# )
# response = llm.complete("介绍一下 qwen-plus 和 qwen-max 的区别")
# print(response)
#
# # 3.1 本地ollama调用  pip install llama-index-llms-ollama    # 加载ollma本地模型
# from llama_index.llms.ollama import Ollama
#
# llm = Ollama(
#     model='qwen2.5:7b',
#     request_timeout=60,   # 默认30秒, 模型响应时间较长, 可适当调大
# )
#
# response = llm.complete("介绍一下 Qwen-Plus 和 Qwen-Max 的区别")
# print(response)






