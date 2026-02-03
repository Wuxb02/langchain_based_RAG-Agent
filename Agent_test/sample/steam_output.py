from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_community.chat_models.tongyi import ChatTongyi



@tool(description="获取股票价格信息，传入股票名称，返回字符串")       # 装饰器定义工具
def get_price(name):
    return f"{name}的价格是100元。"

@tool(description="获取股票信息，传入股票名称，返回字符串")      
def get_info(name):
    return f"{name}是一款A股上市公司。"

agent = create_agent(
    ChatTongyi(model="qwen3-max", temperature=0.1),
    tools = [get_price, get_info],         # 提供工具
    system_prompt="你是一个智能的股票查询助手，请根据用户的问题调用相应的工具获取股票信息。" \
    "并且需要告诉我你的思考过程，让我知道为什么调用某一个工具",
)

# 迭代流式输出
# 每一次迭代都会带上历史信息，因此只要用最后一个
for chunk in agent.stream(
    input={
        "messages": [
            {"role": "user", "content": "查询一下腾讯公司的股票，并介绍一下它。"}
        ]
    },
    stream_mode='values'    # 获取完整返回值
):
    latest_msg = chunk['messages'][-1]
    if latest_msg.content:
        print(type(latest_msg).__name__, latest_msg.content)
    try:
        if latest_msg.tool_calls:
            for tool_call in latest_msg.tool_calls:
                print(tool_call['name'])
    except AttributeError:
        pass