from llama_index.core.base.llms.types import ChatMessage
from llama_index.llms.dashscope import DashScope,DashScopeGenerationModels
import time
from dotenv import load_dotenv
import os

from openai.types.admin.organization import role
from openai.types.conversations import message

load_dotenv()

llm = DashScope(
    model_name=DashScopeGenerationModels.QWEN_PLUS,
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    request_timeout=60,  # 默认30s，模型响应时间较长，可适当调大
)

# 1.2 调用模式1-stream_complete：流式输出，输入类型为纯字符串（prompt), 逐 token 返回，不支持多轮对话
# responses = llm.stream_complete("python是什么类型的语言")
# for chunk in responses:
#      print("类型:", type(chunk))
#      print("repr:", repr(chunk))
#     # time.sleep(0.3)
#     # print(chunk.delta,end='',flush=True)

# 1.3 调用模式2-chat：输入类型为‘ChatMessage列表’，输出类型为完整响应（ChatResponse），支持多轮对话，一次性返回

# message = [
#     ChatMessage(role="user",content="python是什么类型的语言")
# ]
# llm_chat = llm.chat(message)
# print(type(llm_chat))    # chat模式输出类型：llama_index.core.base.llms.types.ChatResponse
# print(repr(llm_chat))
# print(llm_chat)
# print(llm_chat.message.role)
# print(llm_chat.message.content)

# 1.4 调用模式3-stream_chat：输入类型为ChatMessage 列表，逐 token 返回，流式输出，支持多轮对话
messages = [
    ChatMessage(role="user",content='你好')
]
stream_chat = llm.stream_chat(messages)
print(type(stream_chat))
print(repr(stream_chat))
for chunk in stream_chat:
    print(repr(chunk))
    print(chunk.delta,end='',flush=True)

