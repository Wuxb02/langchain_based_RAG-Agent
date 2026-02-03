import streamlit as st
import time
from rag import RagService
import config_data as config

st.title("智能客服")
st.divider()

if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {
            "role": "assistant", "content": "您好！我是智能客服，有什么可以帮助您的吗？",

         }
    ]
# 维护rag实例
if 'rag' not in st.session_state:
    st.session_state['rag'] = RagService()

for msg in st.session_state['messages']:
    st.chat_message(msg["role"]).write(msg["content"])

# 输入栏
prompt = st.chat_input("请输入您的问题：")
if prompt:
    # 获取输入并展示
    st.chat_message("user").write(prompt)
    st.session_state['messages'].append(
        {
            "role": "user", "content": prompt
        }
    )

    temp_list = []
    with st.spinner("智能客服正在思考..."):
        response = st.session_state['rag'].chain.stream({"input": prompt}, config.session_config)

        def capture_stream(response,cache_list):
            for chunk in response:
                cache_list.append(chunk)
                yield chunk # 推出迭代式

        st.chat_message("assistant").write_stream(capture_stream(response,temp_list))    
        st.session_state['messages'].append(
            {
                "role": "assistant", "content": ''.join(temp_list)
            }
        )