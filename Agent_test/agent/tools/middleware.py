from typing import Callable
from utils.prompt_loader import load_system_prompts,load_report_prompts
from utils.logger_handler import logger
from langchain.agents import AgentState
from langchain.agents.middleware import wrap_tool_call,before_model,dynamic_prompt,ModelRequest
from langchain.tools.tool_node import ToolCallRequest
from langchain_core.messages import ToolMessage
from langgraph.types import Command
from langgraph.runtime import Runtime

@wrap_tool_call
def monitor_tool(request: ToolCallRequest , 
                 handler: Callable[[ToolCallRequest], ToolMessage | Command] 
) -> ToolCallRequest | Command:
    '''
    工具执行监控
    
    :param request: 请求的数据封装
    :type request: ToolCallRequest
    :param handler: 请求的函数本身
    :type handler: Callable[[ToolCallRequest], ToolMessage | Command]
    :return: 
    :rtype: ToolCallRequest | Command
    '''
    logger.info(f"[toll monitor]执行工具：{request.tool["name"]}")
    logger.info(f"[toll monitor]传入参数：{request.tool["args"]}")

    try:
        res = handler(request)
        logger.info(f"[toll monitor] 调用{request.tool["name"]}成功")
        # 标记提示词转换，注入信息
        if request.tool_call["name"] == "fill_context_for_report":
            request.runtime.context["report"] = True

        return res
    except Exception as e:
        logger.error(f"[toll monitor] 调用{request.tool["name"]}失败：{str(e)}")
        raise e

@before_model
def log_before_model(
    state: AgentState,
    runtime: Runtime
):
    '''
    模型执行前进行log
    
    :param state: Agent状态记录
    :type state: AgentState
    :param runtime: 整个执行过程的上下文信息
    :type runtime: Runtime
    '''
    logger.info(f"[log_before_model]即将调用模型，带有{len(state['messages'])}条信息。")
    
    logger.debug(f"[log_before_model]{type(state['messages'][-1]).__name__}： {state['messages'][-1].content.strip()}") #每次只取最新的
    
    return 

@dynamic_prompt # 每一次生成提示词前调用此函数
def report_prompt_switch(request:ModelRequest):
    '''
    动态切换提示词 rag <==> report
    '''
    is_report = request.runtime.context.get("report",False)
    if is_report:
        # 生成报告
        return load_report_prompts
    return load_system_prompts
