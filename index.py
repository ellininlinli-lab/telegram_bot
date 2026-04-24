import pickle
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer

def load_pdf(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        t = page.extract_text()
        if t:
            text += t + "\n"
    return text

def split_text(text, size=800):
    return [text[i:i+size] for i in range(0, len(text), size)]

print("📖 читаю PDF...")
text = load_pdf("data.pdf")

print("✂️ разбиваю...")
chunks = split_text(text)

print("🧠 создаю базу...")
vectorizer = TfidfVectorizer()
matrix = vectorizer.fit_transform(chunks)

with open("db/data.pkl", "wb") as f:
    pickle.dump((vectorizer, matrix, chunks), f)

print("✅ база готова")