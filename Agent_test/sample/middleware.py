from langchain.agents import create_agent,AgentState
from langchain.agents.middleware import before_agent, after_agent, before_model, after_model,wrap_model_call,wrap_tool_call
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool
from langgraph.runtime import Runtime
from langchain.agents import create_agent
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool


@tool(description="查询天气，传入城市字符串，返回字符串天气信息")       # 装饰器定义工具
def get_weather(name):
    return f"{name}今天多云，最高气温30度，最低气温22度。"



'''
1.agent执行前:  @before_agent
2.agent执行后:  @after_agent
3.model执行前:  @before_model
4.model执行后:  @after_model
5.工具执行中:   @wrap_tool_call
6.模型执行中：  @wrap_model_call

'''

@before_agent
def log_before_agent(state:AgentState, runtime:Runtime):
    print("=== Before Agent ===")
    print(f"Input:{len(state['messages'])}")
    print("====================")

@after_agent
def log_after_agent(state:AgentState, runtime:Runtime):
    print("=== After Agent ===")
    print(f"Output:{len(state['messages'])}")
    print("====================")

@before_model
def log_before_model(state:AgentState, runtime:Runtime):
    print("=== Before Model ===")
    print(f"Input:{len(state['messages'])}")
    print("====================")

@after_model
def log_after_model(state:AgentState, runtime:Runtime):
    print("=== After Model ===")
    print(f"Output:{len(state['messages'])}")
    print("====================")

@wrap_model_call
def model_call_hook(request, handler):
    print("模型调用")
    return handler(request)

@wrap_tool_call
def tool_call_hook(request, handler):
    print(f"工具调用{request.tool_call['name']}")
    print(f"工具参数{request.tool_call['args']}")
    return handler(request)


@tool(description="获取广州天气信息")       # 装饰器定义工具
def get_weather():
    return "广州今天多云，最高气温30度，最低气温22度。"

agent = create_agent(
    ChatTongyi(model="qwen3-max", temperature=0.1),
    tools = [get_weather],                              # 提供工具
    system_prompt="广州天气如何",
    middleware=[
        log_before_agent,
        log_after_agent,
        log_before_model,
        log_after_model,
        tool_call_hook,
        model_call_hook]
)



res = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "广州今天穿什么衣服合适"}
        ]
    }
)


for msg in res['messages']:
    print(type(msg).__name__, msg.content)  
