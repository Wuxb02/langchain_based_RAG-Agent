'''
Agent_test.utils.prompt_loader 的 Docstring
'''

from config_handler import prompts_conf
from path_tools import get_abs_path
from logger_handle import logger

def load_system_prompts():
    try:
        system_prompts_path = get_abs_path(prompts_conf['main_prompt_path'])
    except KeyError as e:
        logger.error(f"[load_system_prompts] 没有main_prompt_path配置")
        raise e
    
    try:
        return open(system_prompts_path,'r', encoding='utf-8').read()
    except Exception as e:
        logger.error(f"[load_system_prompts] 解析system_prompts_path错误：{str(e)}")
        raise e

def load_rag_prompts():
    try:
        rag_prompts_path = get_abs_path(prompts_conf['rag_summarize_prompt_path'])
    except KeyError as e:
        logger.error(f"[load_rag_prompts] 没有rag_summarize_prompt_path配置")
        raise e
    
    try:
        return open(rag_prompts_path,'r', encoding='utf-8').read()
    except Exception as e:
        logger.error(f"[load_rag_prompts] 解析rag_summarize_prompt_path错误：{str(e)}")
        raise e
    
def load_report_prompts():
    try:
        report_prompts_path = get_abs_path(prompts_conf['report_prompt_path'])
    except KeyError as e:
        logger.error(f"[load_report_prompts] 没有report_prompt_path配置")
        raise e
    
    try:
        return open(report_prompts_path,'r', encoding='utf-8').read()
    except Exception as e:
        logger.error(f"[load_report_prompts] 解析report_prompt_path错误：{str(e)}")
        raise e


if __name__ =='__main__':
    print(load_system_prompts())