import streamlit as st
from openai import OpenAI

st.title("내 첫 LLM 웹앱")

# session_state에 저장
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# API Key 입력창
api_key = st.text_input(
    "OpenAI API Key 입력",
    type="password"
)

# 입력된 키 저장
if api_key:
    st.session_state.api_key = api_key

# 질문 입력
question = st.text_input("질문 입력")

# cache 사용
@st.cache_data
def get_answer(q, key):

    client = OpenAI(api_key=key)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": q}
        ]
    )

    return response.choices[0].message.content

# 버튼
if st.button("질문하기"):

    if not st.session_state.api_key:
        st.warning("API Key를 입력하세요")

    elif not question:
        st.warning("질문을 입력하세요")

    else:
        answer = get_answer(
            question,
            st.session_state.api_key
        )

        st.write("### AI 응답")
        st.write(answer)
