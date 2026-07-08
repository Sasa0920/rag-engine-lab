import streamlit as st

import streamlit as st

def document_card(document):

    st.write(f"**📄 {document['filename']}**")

    status = document["status"]

    if status == "Completed":
        st.success("✅ Completed")

    elif status == "Processing":
        st.info("⏳ Processing")

    elif status == "Pending":
        st.warning("⌛ Pending")

    elif status == "Failed":
        st.error("❌ Failed")

    st.caption(
        f"Uploaded : {document['uploaded_at']}"
    )

    st.markdown("### 📝 Summary")

    if document["summary"]:

        st.info(
            document["summary"]
        )

    else:

        st.warning(
            "Summary is not available yet."
        )
def user_message(text: str):

    with st.chat_message("user"):
        st.markdown(text)

def assistant_message(text: str):

    with st.chat_message("assistant"):
        st.markdown(text)

def loading_message():

    return st.spinner("🤖 AI is thinking...")

def section_title(title: str):

    st.markdown(f"## {title}")