import pickle
import requests
import os
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("CEREBRAS_API_KEY")

with open("db/data.pkl", "rb") as f:
    vectorizer, matrix, chunks = pickle.load(f)


def search(query, k=3):
    q_vec = vectorizer.transform([query])
    scores = cosine_similarity(q_vec, matrix)[0]
    top_idx = scores.argsort()[-k:][::-1]
    return [chunks[i] for i in top_idx]


async def ask_llm(context, question):
    prompt = f"""
Отвечай только по лекциям.

Контекст:
{context}

Вопрос:
{question}
"""

    response = requests.post(
        "https://api.cerebras.ai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama3.1-8b",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        }
    )

    return response.json()["choices"][0]["message"]["content"]