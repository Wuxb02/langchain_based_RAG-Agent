'''
知识库基础服务
'''
import os
import config_data as config
import hashlib
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from datetime import datetime

def check_md5(md5: str) -> bool:
    
    '''
    判断MD5值是否已经存在

    return: True存在，False不存在
    '''
    if not os.path.exists(config.md5_path):
        # 不存在则创建
        open(config.md5_path, "w", encoding="utf-8").close()
        return False
    
    with open(config.md5_path, "r", encoding="utf-8") as f:
        md5_list = f.read().splitlines()
        for line in md5_list:
            line = line.strip() # 去掉字符串前的空格
            if line == md5:
                return True
        return False


def save_md5(md5: str):
    
    '''
    保存MD5值到数据库
    '''
    with open(config.md5_path, "a", encoding="utf-8") as f:
        f.write(md5 + "\n")


def string_md5(string: str, encoding: str = 'utf-8') -> str:
    
    '''
    计算字符串的MD5值
    '''
    # 字符串转bytes
    string_bytes = string.encode(encoding)
    # 计算MD5值
    md5 = hashlib.md5(string_bytes).hexdigest()
    return md5


class KnowledgeBaseService(object):
    
    '''
    知识库基础类
    '''
    
    def __init__(self):
        # 确保数据库文件存在，不存在则创建
        os.makedirs(config.persist_directory, exist_ok=True) 
        #数据库实例
        self.chroma = Chroma(
            collection_name=config.collection_name,
            embedding_function=DashScopeEmbeddings(model="text-embedding-v3"),
            persist_directory=config.persist_directory
        )    
        #文本分割器实例
        self.spliter = RecursiveCharacterTextSplitter(  
            chunk_size=config.chunk_size, 
            chunk_overlap=config.chunk_overlap,
            separators=config.separators,
            length_function=len
            ) 

    
    def upload_by_str(self, data: str, file_name: str) -> str:
        '''
        通过字符串向量化后上传内容到知识库
        '''
        # 1. 计算MD5值，判断是否已经存在
        md5 = string_md5(data)
        if check_md5(md5):
            return f"内容已存在，跳过上传"

        if len(data) > config.max_split_char_number:
            knowledge = self.spliter.split_text(data)
        else:
            knowledge = [data]

        metadata = {
            'source': file_name,
            'create time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        self.chroma.add_texts(      # 内容就加载到向量库中了
            # iterable -> list \ tuple
            knowledge,
            metadatas=[metadata] * len(knowledge)
        )

        save_md5(md5)
        return f"文件 {file_name} 上传成功"


if __name__ == "__main__":
    service = KnowledgeBaseService()
    test_str = "这是一个测试字符串，用于测试知识库上传功能。"
    result = service.upload_by_str(test_str, "test_file.txt")
    print(result)   