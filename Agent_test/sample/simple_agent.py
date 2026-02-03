from langchain.agents import create_agent
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool


@tool(description="获取广州天气信息")       # 装饰器定义工具
def get_weather():
    return "广州今天多云，最高气温30度，最低气温22度。"

agent = create_agent(
    ChatTongyi(model="qwen3-max", temperature=0.1),
    tools = [get_weather],                              # 提供工具
    system_prompt="广州天气如何",
)



res = agent.invoke(
    {
        "message": [
            {"role": "user", "content": "你好，能帮我回答一个问题吗？"}
        ]
    }
)


for msg in res['messages']:
    print(type(msg).__name__, msg.content)  
# print
# AIMessage 
# ToolMessage 广州今天多云，最高气温30度，最低气温22度。
# AIMessage 广州今天天气多云，最高气温为30℃，最低气温为22℃。建议根据气温变化适当增减 衣物，并注意防晒。