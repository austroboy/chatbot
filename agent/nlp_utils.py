import re
import numpy as np
from langdetect import detect, DetectorFactory
from sentence_transformers import SentenceTransformer

DetectorFactory.seed = 0

model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

def detect_language(text: str) -> str:
    try:
        lang = detect(text)
    except Exception:
        lang = 'en'
    return 'bn' if lang == 'bn' else 'en'

def transliterate_to_bangla(text: str) -> str:
    # indic না থাকলে fallback: same text return
    return text

def get_embedding(text: str):
    return model.encode(text)

def retrieve_top_k(query_embedding, k=5):
    from .models import KnowledgeBase
    entries = KnowledgeBase.objects.all()
    if not entries:
        return []
    similarities = []
    for entry in entries:
        if entry.embedding:
            emb = np.array(entry.embedding, dtype=np.float32)
            sim = float(np.dot(query_embedding, emb) / (np.linalg.norm(query_embedding) * np.linalg.norm(emb)))
            similarities.append((sim, entry))
    similarities.sort(key=lambda x: x[0], reverse=True)
    return [entry for sim, entry in similarities[:k]]

def get_answer(query: str):
    q = query.strip()
    q_embedding = get_embedding(q)
    top = retrieve_top_k(q_embedding, k=1)
    if top:
        best = top[0]
        return best.answer, 0.95
    return "Sorry, I couldn't find an answer. Please contact support.", 0.0