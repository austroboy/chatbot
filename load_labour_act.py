import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_agent.settings')
django.setup()

from agent.rag_engine import get_rag_engine

# RAG engine initialize করুন
rag = get_rag_engine()

# Labour Act টেক্সট লোড করুন
with open('data/labour_act.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Vector store তৈরি করুন
rag.load_from_text(text)
print("✅ Labour Act loaded successfully!")

# টেস্ট কোয়েরি
question = "Which types of government or government-controlled institutions have been excluded from the scope of this Act?"
result = rag.query(question)
print(f"\n📝 Question: {question}")
print(f"\n✅ Answer: {result['answer']}")