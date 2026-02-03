'''
构建核心rag
'''
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda
from file_history import get_history
from vector_stroes import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi

class RagService(object):
    def __init__(self):
        self.vector_store = VectorStoreService(embedding_model=DashScopeEmbeddings(model=config.embedding_model))
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", "你是一个专业的知识问答助手，根据用户的问题和提供的上下文信息进行简短回答。上下文信息：{context}\n\n"),
            ("system", "对话历史记录如下：{history}\n\n"),
            ("user", "用户问题：{question}")
        ])
        self.chat_model = ChatTongyi(model=config.chat_model, temperature=0.1)
        self.chain = self._get_chain()
    


    
    def _get_chain(self):\
        # 获取检索器

        def format_for_retriever(value: dict) -> str:
            print("=== Prompt ===")
            print(value)
            print("==============")
            return value["input"]

        def format_for_template(value: dict) -> dict:
            '''
            拼接上下文和问题
            '''
            context = value['context']
            question = value['question']['input']
            history = value['question']['history']
            return {
                'question': question,
                'context': context,
                'history': history
            }

        def print_prompt(prompt):
            print("=== Prompt ===")
            print(prompt.to_string())
            print("==============")
            return prompt
        
        def format_document(docs: list[Document]):
            if not docs:
                return "暂无相关内容。"
            context = "\n".join([doc.page_content for doc in docs])
            return context

        retriever = self.vector_store.get_retriever()

        chain = (
            {
                'context': RunnableLambda(format_for_retriever) | retriever | format_document, 
                'question': RunnablePassthrough() 
            }  | RunnableLambda(format_for_template) | self.prompt_template | print_prompt |self.chat_model | StrOutputParser()

        )
        # 附带历史信息的增强链
        # RunnableWithMessageHistory 会劫持输入，添加历史消息
        # 添加前输入：{'question': '用户问题'}
        # 添加后输入：{'question': '用户问题', 'history': []}
        runnable_with_history = RunnableWithMessageHistory(
            chain,
            get_history,
            session_id_key="question",
            history_messages_key="history"
        )
        return runnable_with_history
        



if __name__ == "__main__":
    # sessionid
    session_config = {
        "configurable": {
            "session_id": "user_001"
        }
    }
    rag_service = RagService()
    # 目前输入为：{'input': '我身高170cm，尺码推荐', 'history': []}
    res = rag_service.chain.invoke({'input': '我身高170cm，尺码推荐'}, session_config)
    print(res)
