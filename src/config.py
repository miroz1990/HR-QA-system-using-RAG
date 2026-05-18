import os
import streamlit as st

# Embedding model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# FAISS config
TOP_K = 20

# Chunking
CHUNK_SIZE = 300
CHUNK_OVERLAP = 50

MODEL_NAME = "meta-llama/llama-3.2-3b-instruct"
# OPENROUTER_API_KEY = st.secrets.get(
#     "OPENROUTER_API_KEY",
#     os.getenv("OPENROUTER_API_KEY")
# )



# try:
#     OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
# except Exception:
#     OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# OPENROUTER_API_KEY = st.secrets.get("OPENROUTER_API_KEY") or os.getenv("OPENROUTER_API_KEY")

# if not OPENROUTER_API_KEY:
#     raise ValueError("OPENROUTER_API_KEY is missing. Check .streamlit/secrets.toml")

# print("KEY LOADED:", OPENROUTER_API_KEY is not None)



# print("CONFIG KEY:", OPENROUTER_API_KEY)