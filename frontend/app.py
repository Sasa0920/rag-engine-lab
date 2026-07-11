import time
import streamlit as st

from api import (
    upload_pdf,
    ask_question,
    stream_answer,
    list_documents,
    get_document,
    check_backend,
)

from components import (
    document_card,
)

st.set_page_config(
    page_title="DocuMind AI",
    page_icon="📄",
    layout="wide"
)

if "selected_document_id" not in st.session_state:
    st.session_state.selected_document_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("📄 DocuMind AI")
st.caption("AI-powered PDF Question Answering System")

if check_backend():
    st.success("✅ Backend Connected")
else:
    st.error("❌ Cannot connect to FastAPI backend")
    st.stop()

with st.sidebar:

    st.header("📤 Upload PDF")
    uploaded_file = st.file_uploader(
        "Choose a PDF",
        type=["pdf"]
    )

    if st.button(
        "Upload PDF",
        use_container_width=True
    ):
        if uploaded_file is None:
            st.warning("Please choose a PDF.")
        else:
            with st.spinner("Uploading PDF..."):
                result = upload_pdf(uploaded_file)

            st.success(result["message"])
            st.session_state.selected_document_id = result["tasks"][0]["document_id"]
            st.rerun()

    st.divider()

    st.header("📑 Documents")

    documents = list_documents()

    if documents:
        options = ["All documents"] + [doc["filename"] for doc in documents]
        current_index = 0
        if st.session_state.selected_document_id is not None:
            for index, doc in enumerate(documents, start=1):
                if doc["id"] == st.session_state.selected_document_id:
                    current_index = index
                    break

        selected_label = st.selectbox(
            "Current Document",
            options=options,
            index=current_index,
            key="document_selector"
        )

        if selected_label == "All documents":
            st.session_state.selected_document_id = None
        else:
            selected_doc = next(doc for doc in documents if doc["filename"] == selected_label)
            st.session_state.selected_document_id = selected_doc["id"]

        for doc in documents:
            if doc["id"] == st.session_state.selected_document_id:
                st.info(f"🔎 Active: {doc['filename']}")
                break

        selected_document = None
        if st.session_state.selected_document_id is not None:
            selected_document = next(
                (doc for doc in documents if doc["id"] == st.session_state.selected_document_id),
                None
            )

        if selected_document:
            document_card(selected_document)

            # Auto refresh while Celery is processing
            if selected_document["status"] == "Processing":
                st.info(
                    "⏳ Processing document...\n\nRefreshing every 3 seconds."
                )
                time.sleep(3)
                st.rerun()
    else:
        st.info("No documents uploaded yet.")

st.subheader("💬 AI Assistant")

# Display previous conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input(
    "Ask anything about your uploaded document..."
)

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        status_placeholder = st.empty()
        content_placeholder = st.empty()

        status_placeholder.info("🤖 Generating answer...")

        # True token streaming
        chunks = []

        for chunk in stream_answer(
            prompt,
            document_id=st.session_state.selected_document_id
        ):

            chunks.append(chunk)

            answer = "".join(chunks)

            content_placeholder.markdown(answer + "▌")

        full_answer = "".join(chunks)

        content_placeholder.markdown(full_answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": full_answer
        }
    )