# from django.apps import AppConfig


# class AgentConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'agent'

# agent/apps.py
import os
from django.apps import AppConfig

class AgentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'agent'

    def ready(self):
        from .rag_engine import get_rag_engine
        rag = get_rag_engine()
        # Check if vector store already exists
        if not os.path.exists("./chroma_db"):
            try:
                with open("data/labour_act.txt", "r", encoding="utf-8") as f:
                    text = f.read()
                rag.load_from_text(text)
                rag.create_qa_chain()
                print("✅ RAG engine ready with documents.")
            except Exception as e:
                print(f"⚠️ RAG init failed: {e}")
        else:
            # Load existing vector store
            from langchain_community.vectorstores import Chroma
            rag.vector_store = Chroma(
                embedding_function=rag.embeddings,
                persist_directory="./chroma_db"
            )
            rag.create_qa_chain()
            print("✅ RAG engine loaded from existing vector store.")