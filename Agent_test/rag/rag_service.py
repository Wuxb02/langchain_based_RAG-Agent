'''
rag总结服务
结合参考资料和用户提问让模型进行总结概括
'''
from rag.vector_store import VectorStoreService
from utils.prompt_loader import load_rag_prompts
from langchain_core.prompts import PromptTemplate
from model.factory import chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document


class RagSummarizeService(object):

    def __init__(self):
        self.vector_store = VectorStoreService()
        self.retriever = self.vector_store.get_retriever()
        self.promp_txt = load_rag_prompts()
        self.prompt_template = PromptTemplate.from_template(self.promp_txt)
        self.model = chat_model
        self.chain = self._init_chain()

    def _init_chain(self):
        def temp(values) :
            print('temp',values.to_string())
            return values
        chain = self.prompt_template | temp | self.model | StrOutputParser()
        return chain
    
    def retriever_docs(self,query:str) -> list[Document]:
        return self.retriever.invoke(query)
    

    def rag_summarize(self, query:str) -> str:
        context_docs = self.retriever_docs(query)

        context = ""
        counter = 0
        for doc in context_docs:
            counter+=1
            context +=f"\n\n【参考资料{counter}】: 参考内容：{doc.page_content} | 元数据：{doc.metadata}"
        
        return self.chain.invoke({
            "input":  query,
            "context": context
        })


if __name__ == "__main__":
    rag = RagSummarizeService()
    print(rag.rag_summarize('小户型适合什么扫地机'))