'''
Agent_test.rag.vector_store 的 Docstring
'''
import os
from langchain_chroma import Chroma
from utils.config_handler import chroma_conf
from utils.path_tools import get_abs_path
from utils.file_handler import txt_loader, pdf_loader, listdit_with_allowed_type, get_file_md5_hex

from utils.logger_handle import logger
from model.factory import embed_model

from langchain_text_splitters import RecursiveCharacterTextSplitter

import hashlib


class VectorStoreService:
    def __init__(self):
        # 数据库对象
        self.vector_store = Chroma(
            collection_name=chroma_conf["collection_name"],
            persist_directory=chroma_conf["persist_directory"],
            embedding_function=embed_model
        )

        # 分割对象
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_conf["chunk_size"],
            chunk_overlap=chroma_conf["chunk_overlap"],
            separators=chroma_conf["separators"],
            length_function=len
        )

    def get_retriever(self):
        '''
        配置检索器
        '''
        return self.vector_store.as_retriever(
            search_kwargs={
                "k": chroma_conf["k"]
            }
        )

    def load_document(self):
        '''
        读取文件存入数据库
        '''

        def check_md5_hex(md5_for_check: str) -> bool:
            '''
            检查是否存在
            '''
            if not os.path.exists(get_abs_path(chroma_conf["md5_hex_store"])):
                open(get_abs_path(
                    chroma_conf["md5_hex_store"]), 'w', encoding='utf-8').close()
                return False
            with open(get_abs_path(chroma_conf["md5_hex_store"]), 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    line = line.strip()
                    if line == md5_for_check:
                        return True
            return False

        def save_md5(md5_for_check: str) -> None:
            '''
            保存md5

            :param md5_for_check: 说明
            :type md5_for_check: str
            '''
            with open(get_abs_path(chroma_conf["md5_hex_store"]), 'a', encoding='utf-8') as f:
                f.write(md5_for_check+"\n")

        def get_file_documents(filepath: str):
            if filepath.endswith('txt'):
                return txt_loader(filepath)
            elif filepath.endswith('pdf'):
                return pdf_loader(filepath,password=None)
            return []

        allowed_file_path = listdit_with_allowed_type(chroma_conf["data_path"],
                                                      tuple(chroma_conf["allow_knowledge_file_type"]))

        for path in allowed_file_path:
            # 获取md5
            md5 = get_file_md5_hex(path)
            if check_md5_hex(md5):
                logger.info(f"[加载知识库] {path}已经存在于数据库")
                continue
            try:
                documents = get_file_documents(path)
                if not documents:
                    logger.info(f"[加载知识库] {path}内没有有效文本")
                    continue
                # 文本分割
                split_document = self.splitter.split_documents(documents)

                if not split_document:
                    logger.info(f"[文本分割] {path}分割后没有有效文本")
                    continue

                # 存入向量数据库
                # ================= 核心修改开始 =================
                # 2. 生成基于内容的唯一 ID
                ids = []
                for doc in split_document:
                    # 将页面内容和元数据（如source）组合起来进行哈希
                    # 这样如果内容没变，ID 永远一样
                    doc_content = doc.page_content + str(doc.metadata.get('source', ''))
                    doc_hash = hashlib.md5(doc_content.encode('utf-8')).hexdigest()
                    ids.append(doc_hash)

                # 3. 存入向量数据库时显式传入 ids
                # Chroma 的机制：如果 ID 已存在，会更新（Update）；如果不存在，会添加（Add）。
                # 这完美解决了重复问题。
                self.vector_store.add_documents(documents=split_document, ids=ids)
                # ================= 核心修改结束 =================

                save_md5(md5)

                logger.info(f"[加载知识库] {path}加载成功")
            except Exception as e:
                # exc_info=True: 详细报错（堆栈）
                logger.error(f"[加载知识库] {path}加载失败：{str(e)}", exc_info=True)


if __name__ == '__main__':
    vs = VectorStoreService()
    vs.load_document()

    retriever = vs.get_retriever()
    res = retriever.invoke('扫地机器人')
    for r in res:
        print(r)