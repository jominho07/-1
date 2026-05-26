import streamlit as st
from openai import OpenAI

st.title("Chat 페이지")

# API Key 저장용
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# 대화 저장용
if "messages" not in st.session_state:
    st.session_state.messages = []

# API Key 입력
api_key = st.text_input(
    "OpenAI API Key 입력",
    type="password"
)

# session_state 저장
if api_key:
    st.session_state.api_key = api_key

# Clear 버튼
if st.button("Clear"):

    st.session_state.messages = []

    st.success("대화가 초기화되었습니다")

# 이전 대화 출력
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 사용자 입력
prompt = st.chat_input("메시지를 입력하세요")

# 메시지 입력 시
if prompt:

    # 사용자 메시지 저장
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # 사용자 메시지 출력
    with st.chat_message("user"):
        st.write(prompt)

    # API Key 확인
    if not st.session_state.api_key:

        st.warning("API Key를 입력하세요")

    else:

        client = OpenAI(
            api_key=st.session_state.api_key
        )

        # OpenAI Responses API 사용
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        answer = response.output_text

        # AI 메시지 저장
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        # AI 메시지 출력
        with st.chat_message("assistant"):
            st.write(answer)
