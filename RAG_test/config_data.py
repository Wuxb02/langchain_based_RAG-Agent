'''

'''

md5_path = "./md5_store.txt"


# 数据库
collection_name = 'test_collection'
persist_directory = "./chroma_db"


# 字符分割
chunk_size = 1000          # 每个文本块的最大字符数
chunk_overlap = 100        # 文本
separators = ["\n\n", "\n", "。", "！", "？", ".", "!", "?", " ", ""]  # 分割符号
max_split_char_number = 10000    # 最大分割字符数


# 检索器配置
retriever_k = 1


embedding_model = "text-embedding-v4"
chat_model = "qwen3-max"

# 配置文件
session_config = {
    "configurable": {
        "session_id": "user_001"
    }
}