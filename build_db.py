import os
import pickle
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer

PDF_PATH = "data.pdf"

print("📖 читаю PDF...")

reader = PdfReader(PDF_PATH)

texts = []
for page in reader.pages:
    text = page.extract_text()
    if text:
        texts.append(text)

# делим на куски
chunks = []
for text in texts:
    for i in range(0, len(text), 500):
        chunks.append(text[i:i+500])

print(f"🔹 чанков: {len(chunks)}")

vectorizer = TfidfVectorizer()
matrix = vectorizer.fit_transform(chunks)

os.makedirs("db", exist_ok=True)

with open("db/data.pkl", "wb") as f:
    pickle.dump((vectorizer, matrix, chunks), f)

print("✅ База готова")