'''
基于Streamlit的文件上传应用服务
'''

import time
import streamlit as st
from knowledge_base import KnowledgeBaseService
# streamlit run app_file_uploader.py


# 添加标题
st.title("知识库更新服务")

# 添加文件上传组件
uploaded_file = st.file_uploader(
    '上传文件进行知识库更新',
    type=['txt'],
    accept_multiple_files=False  # 只允许上传单个txt文件
)

# sesstion_state用于存储上传的文件内容(一个字典)
if 'service' not in st.session_state:
    st.session_state['service'] = KnowledgeBaseService()



if uploaded_file is not None:
    # 获取到文件
    file_name = uploaded_file.name
    file_size = uploaded_file.size/1024 # 转换为KB
    file_type = uploaded_file.type
    st.subheader("文件信息")
    st.write(f"文件名: {file_name} | 文件大小: {file_size:.2f} KB | 文件类型: {file_type}")

    file_content = uploaded_file.getvalue().decode("utf-8")  # 获取文件的二进制内容并解码为字符串
    st.subheader("文件内容预览")
    st.text_area("文件内容", value=file_content, height=300)
    
    with st.spinner('正在更新知识库...'):
        time.sleep(1)  # 模拟处理时间
        result = st.session_state['service'].upload_by_str(file_content, file_name)  # 调用服务实例的更新方法
        st.write(result)  # 显示结果
