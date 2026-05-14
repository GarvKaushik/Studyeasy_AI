

import streamlit as st
import requests

BACKEND_URL = st.secrets["BACKEND_URL"]

UPLOAD_ENDPOINT = f"{BACKEND_URL}/upload"
CHAT_ENDPOINT = f"{BACKEND_URL}/chat"



st.set_page_config(
    page_title="Studyeasy AI - RAG ",
    page_icon="📚",
    layout="wide"
)



if "session_id" not in st.session_state:
    st.session_state.session_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []



st.title("📚 Studyeasy AI")
st.markdown(
    "Upload your notes or PDFs and ask questions from them."
)


with st.sidebar:

    st.header("Upload Notes")

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if st.button("Upload PDF"):

        if uploaded_file is None:
            st.warning("Please upload a PDF first.")

        else:

            with st.spinner("Uploading and processing PDF..."):

                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        "application/pdf"
                    )
                }

                try:

                    response = requests.post(
                        UPLOAD_ENDPOINT,
                        files=files,
                        timeout=300
                    )

                    if response.status_code == 200:

                        data = response.json()

                        st.session_state.session_id = data[
                            "session_id"
                        ]

                        st.success(
                            "PDF uploaded successfully!"
                        )

                    else:

                        st.error(
                            f"Upload failed: {response.text}"
                        )

                except Exception as e:

                    st.error(str(e))

    st.divider()

    st.subheader("Current Session")

    if st.session_state.session_id:
        st.code(st.session_state.session_id)
    else:
        st.info("No active session")



for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])



prompt = st.chat_input(
    "Ask a question from your notes..."
)



if prompt:

    if not st.session_state.session_id:

        st.warning(
            "Please upload a PDF first."
        )

    else:

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.markdown(prompt)


        
        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                payload = {
                    "question": prompt,
                    "session_id": (
                        st.session_state.session_id
                    ),
                    "top_k": 8,
                    "min_score": 0.2,
                    "summarize": True
                }

                try:

                    response = requests.post(
                        CHAT_ENDPOINT,
                        json=payload,
                        timeout=300
                    )

                    if response.status_code == 200:

                        data = response.json()

                        answer = data.get(
                            "answer",
                            "No answer returned."
                        )

                        summary = data.get(
                            "summary"
                        )

                        citations = data.get(
                            "citations",
                            []
                        )

                        st.markdown(answer)

                        if summary:

                            st.subheader(
                                "Quick Summary"
                            )

                            st.info(summary)

                        if citations:

                            st.subheader("Sources")

                            for citation in citations:
                                st.markdown(
                                    f"- {citation}"
                                )

                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": answer
                        })

                    else:

                        st.error(response.text)

                except Exception as e:

                    st.error(str(e))
