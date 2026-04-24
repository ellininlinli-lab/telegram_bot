import pickle
import os
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
from cerebras.cloud.sdk import Cerebras

load_dotenv()

API_KEY = os.getenv("CEREBRAS_API_KEY")
print("API_KEY =", API_KEY)

client = Cerebras(api_key=API_KEY)

with open("db/data.pkl", "rb") as f:
    vectorizer, matrix, chunks = pickle.load(f)


def search(query, k=3):
    q_vec = vectorizer.transform([query])
    scores = cosine_similarity(q_vec, matrix)[0]
    top_idx = scores.argsort()[-k:][::-1]
    return [chunks[i] for i in top_idx]


def ask_llm(context, question):
    prompt = f"""
Отвечай только по лекциям.

Контекст:
{context}

Вопрос:
{question}
"""

    try:
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3.1-8b",
            max_completion_tokens=512,
            temperature=0.2
        )

        return completion.choices[0].message.content

    except Exception as e:
        return f"❌ Ошибка API: {str(e)}"