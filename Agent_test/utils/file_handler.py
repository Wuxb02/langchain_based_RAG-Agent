'''
文件处理
'''

import os
import hashlib
from logger_handle import logger
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader,TextLoader


def get_file_md5_hex(filepath: str):
    '''
    获取MD十六进制字符串
    '''
    if not os.path.exists(filepath):
        logger.error(f"[md5计算], 文件{filepath}不存在")
        return 
    if not os.path.isfile(filepath):
        logger.error(f"[md5计算], {filepath}非文件路径")
        return 
    md5_obj = hashlib.md5()
    # 流式更新MD5
    chunck_size = 4096
    try:
        with open(filepath,'rb') as f:  #二进制读取
            # chunk = f.read(chunck_size)
            # while chunk:
            #     ....
            while chunk := f.read(chunck_size): 
                md5_obj.update(chunk)
            md5_hex = md5_obj.hexdigest()
            return md5_hex
    except Exception as e:
        logger.error(f'计算文件{filepath}异常')
        return None


def listdit_with_allowed_type(path:str, allowed_type:tuple[str]):
    '''
    返回文件列表
    '''
    files = []
    if not os.path.isdir():
        logger.error(f"[listdit_with_allowed_type]： 当前{path}非文件夹")
        return allowed_type

    for f in os.listdir(path):
        if f.endswith(allowed_type):
            files.append(os.path.join(path,f))
    return tuple(files) #不允许修改


def pdf_loader(filepath: str, password:str) -> list[Document]:
    '''
    读取pdf
    '''
    return PyPDFLoader(filepath,password).load()

def txt_loader(filepath: str) -> list[Document]:
    '''
    读取txt
    '''
    return TextLoader(filepath).load()