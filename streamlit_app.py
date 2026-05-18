import streamlit as st
from src.reranker import Reranker
from src.rag_pipeline import load_pipeline, ask


reranker = Reranker()

# Load once
@st.cache_resource
def init_pipeline():
    return load_pipeline()

retriever = init_pipeline()


def auto_filter_query(query):
    query = query.lower()

    if any(word in query for word in ["leave", "vacation"]):
        return {"role": "employee", "doc_type": "leave_policy"}

    if any(word in query for word in ["security", "data", "password"]):
        return {"doc_type": "it_security_policy"}

    if any(word in query for word in ["conduct", "harassment"]):
        return {"doc_type": "code_of_conduct"}

    return None


# UI
st.set_page_config(page_title="HR Assistant", layout="wide")

st.title("🏢 TechNova HR Assistant (RAG System)")
st.write("Ask questions about company policies")

query = st.text_input("💬 Ask a question:")

if query:
    filters = auto_filter_query(query)

    answer, contexts = ask(query, retriever, reranker, filters)

    st.subheader("🤖 Answer")
    st.write(answer)

    st.subheader("📚 Sources")

    for c in contexts:
        with st.expander(f"{c['source']} "):
        # with st.expander(f"{c['source']} (section {c.get('section')})"):
            st.write(c["text"])