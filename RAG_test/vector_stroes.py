'''
主要用于提供检索器
'''
from langchain_chroma import Chroma
import config_data as config
from langchain_community.embeddings import DashScopeEmbeddings

class VectorStoreService(object):
    
    '''
    向量数据库基础类
    '''
    
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model  

        self.vector_store = Chroma(
            collection_name=config.collection_name,
            embedding_function=embedding_model,
            persist_directory=config.persist_directory
        )
    
    def get_retriever(self, search_type: str = 'similarity'):
        '''
        获取检索器
        
        search_type: 检索类型，支持'similarity'和'distance'
        search_kwargs: 检索参数
        return: 检索器实例
        '''
        retriever = self.vector_store.as_retriever(
            search_type=search_type,
            search_kwargs={
                "k": config.retriever_k
            }
        )
        return retriever
    

if __name__ == "__main__":
    embedding_model = DashScopeEmbeddings(model="text-embedding-v4")
    vector_store_service = VectorStoreService(embedding_model=embedding_model)
    retriever = vector_store_service.get_retriever()
    print(retriever.invoke("体重180斤"))
