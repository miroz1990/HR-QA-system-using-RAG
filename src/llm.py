import os
import requests
import streamlit as st
from src.config import MODEL_NAME


def get_api_key():
    return st.secrets.get("OPENROUTER_API_KEY") or os.getenv("OPENROUTER_API_KEY")


def generate_answer(prompt):
    api_key = get_api_key()

    if not api_key:
        raise ValueError("OPENROUTER_API_KEY is missing")

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 120,
        "temperature": 0,
    }

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    if "choices" not in data:
        raise Exception(f"LLM Error: {data}")

    return data["choices"][0]["message"]["content"]