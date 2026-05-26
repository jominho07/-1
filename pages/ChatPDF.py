import streamlit as st
from openai import OpenAI
import tempfile

st.title("ChatPDF")

# API Key 저장
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# vector store 저장
if "vector_store_id" not in st.session_state:
    st.session_state.vector_store_id = None

# API Key 입력
api_key = st.text_input(
    "OpenAI API Key 입력",
    type="password"
)

if api_key:
    st.session_state.api_key = api_key

# PDF 업로드
uploaded_file = st.file_uploader(
    "PDF 파일 업로드",
    type="pdf"
)

# OpenAI 연결
if st.session_state.api_key:

    client = OpenAI(
        api_key=st.session_state.api_key
    )

    # PDF 업로드 시
    if uploaded_file is not None:

        # 임시 파일 저장
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as tmp_file:

            tmp_file.write(uploaded_file.read())

            temp_path = tmp_file.name

        # OpenAI 파일 업로드
        file = client.files.create(
            file=open(temp_path, "rb"),
            purpose="assistants"
        )

        # vector store 생성
        vector_store = client.vector_stores.create(
            name="chatpdf_store"
        )

        # vector store에 파일 추가
        client.vector_stores.files.create(
            vector_store_id=vector_store.id,
            file_id=file.id
        )

        # 저장
        st.session_state.vector_store_id = vector_store.id

        st.success("PDF 업로드 완료")

# 질문 입력
question = st.text_input("질문 입력")

# 질문 버튼
if st.button("질문하기"):

    if not st.session_state.vector_store_id:

        st.warning("PDF를 먼저 업로드하세요")

    else:

        client = OpenAI(
            api_key=st.session_state.api_key
        )

        # Responses API + File Search
        response = client.responses.create(
            model="gpt-4.1-mini",

            input=question,

            tools=[
                {
                    "type": "file_search",
                    "vector_store_ids": [
                        st.session_state.vector_store_id
                    ]
                }
            ]
        )

        answer = response.output_text

        st.write("### 답변")
        st.write(answer)

# Clear 버튼
if st.button("Clear"):

    if st.session_state.vector_store_id:

        client = OpenAI(
            api_key=st.session_state.api_key
        )

        # vector store 삭제
        client.vector_stores.delete(
            st.session_state.vector_store_id
        )

        st.session_state.vector_store_id = None

        st.success("Vector Store 삭제 완료")
