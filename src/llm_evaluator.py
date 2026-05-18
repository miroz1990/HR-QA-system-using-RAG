import os
import json
from turtle import st
import requests

API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "meta-llama/llama-3.2-3b-instruct"

def get_api_key():
    try:
        return st.secrets["OPENROUTER_API_KEY"]
    except Exception:
        return os.getenv("OPENROUTER_API_KEY")
    
def evaluate_with_llm(question, answer, reference, context):
    prompt = f"""
You are an expert evaluator for a RAG system.

Return ONLY valid JSON. No markdown. No explanation outside JSON.

Evaluate this answer using scores from 1 to 5.

Question:
{question}

Reference Answer:
{reference}

Generated Answer:
{answer}

Context:
{context}

Return exactly this JSON format:
{{
  "correctness": 1,
  "grounding": 1,
  "relevance": 1,
  "explanation": "max 10 words"
}}
"""
    api_key = get_api_key()

    if not api_key:
        raise ValueError("OPENROUTER_API_KEY is missing")
    response = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL_NAME,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 200,
            "temperature": 0,
        },
    )

    data = response.json()

    if "error" in data:
        raise Exception(f"Evaluator LLM Error: {data}")

    content = data["choices"][0]["message"]["content"]

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        raise ValueError(f"Evaluator did not return valid JSON:\n{content}")