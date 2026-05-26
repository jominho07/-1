import streamlit as st
from openai import OpenAI

st.title("국립부경대학교 도서관 규정 챗봇")

# API Key 저장
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# API Key 입력
api_key = st.text_input(
    "OpenAI API Key 입력",
    type="password"
)

if api_key:
    st.session_state.api_key = api_key

# 도서관 규정
library_rules = """
학부생은 최대 5권까지 대출 가능하다.
대출 기간은 14일이다.
대학원생은 최대 10권까지 대출 가능하다.
도서관 휴관일은 공휴일 및 지정일이다.
연체 시 연체일수만큼 대출이 제한된다.
"""

# 질문 입력
question = st.text_input(
    "도서관 규정에 대해 질문하세요"
)

# 버튼 클릭 시
if st.button("질문하기"):

    # 질문 확인
    if not question:

        st.warning("질문을 입력하세요")

    # API Key 확인
    elif not st.session_state.api_key:

        st.warning("API Key를 입력하세요")

    else:

        client = OpenAI(
            api_key=st.session_state.api_key
        )

        # 규정 기반 답변
        response = client.responses.create(
            model="gpt-4.1-mini",

            input=f"""
다음은 국립부경대학교 도서관 규정입니다.

{library_rules}

반드시 위 규정 내용을 기반으로만 답변하세요.

질문:
{question}
"""
        )

        answer = response.output_text

        st.write("### 답변")
        st.write(answer)
