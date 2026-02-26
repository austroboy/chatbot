# agent/rag_engine.py
import os
from dotenv import load_dotenv
import traceback

load_dotenv()  # .env ফাইল থেকে ভেরিয়েবল লোড করে

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Groq (optional)
try:
    from langchain_groq import ChatGroq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

# Local LLM (optional)
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import torch


class RAGEngine:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )
        self.vector_store = None
        self.qa_chain = None
        self.llm = None
        self._init_llm()

    def _init_llm(self):
        import os
        GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
        try:
            from langchain_groq import ChatGroq
            self.llm = ChatGroq(
                model="llama-3.3-70b-versatile",  # ✅ নতুন মডেল
                temperature=0,
                api_key=GROQ_API_KEY
            )
            print("✅ Using Groq LLM (fast) with llama-3.3-70b-versatile")
            return
        except Exception as e:
            print(f"⚠️ Groq failed: {e}")
        
        self.llm = None
        print("✅ Using retrieval-only mode (fast)")

        # 2. Fallback to local model (requires accelerate)
        try:
            model_name = "microsoft/phi-2"
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float32,
                device_map="auto"
            )
            pipe = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                max_new_tokens=256,
                temperature=0.1,
                do_sample=False,
            )
            self.llm = HuggingFacePipeline(pipeline=pipe)
            print("✅ Using local Phi-2 model")
        except Exception as e:
            print(f"[WARN] Local model failed: {e}")
            print("[WARN] Falling back to retrieval-only mode (no generation).")
            self.llm = None

    def load_document(self, file_path: str):
        if file_path.lower().endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        else:
            loader = TextLoader(file_path, encoding="utf-8")
        return loader.load()

    def create_vector_store(self, documents):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""],
        )
        chunks = text_splitter.split_documents(documents)
        print(f"Created {len(chunks)} chunks")
        self.vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory="./chroma_db",
        )
        return self.vector_store

    def create_qa_chain(self):
        if not self.vector_store:
            raise ValueError("Vector store not initialized. Load documents first.")

        retriever = self.vector_store.as_retriever(search_kwargs={"k": 10})

        if not self.llm:
            # retrieval-only mode: qa_chain is just the retriever
            self.qa_chain = retriever
            return

        # Generative mode with LLM
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert on Bangladesh Labour Act.
        Answer questions based on the provided context.
        If the question requires calculation, follow these steps:
        1. Extract the relevant rule from the context (e.g., "1 day leave for every 18 days work").
        2. Gather necessary data from the question (dates, days enjoyed).
        3. Perform the calculation step by step.
        4. Provide the final answer with explanation.

        For example:
        Question: "If I joined on July 7, 2023 and today is Dec 31, 2025; I have enjoyed 5 annual leave; what is my current annual leave balance?"
        Steps:
        - From context: Annual leave is 1 day for every 18 days of work.
        - From join date to current date: calculate total days = (Dec 31, 2025 - July 7, 2023) = 908 days (approx).
        - Earned leave = 908 // 18 = 50 days (since 18*50=900, remainder 8 days).
        - Enjoyed leave = 5 days.
        - Balance = 50 - 5 = 45 days.
        Answer: 45 days.

        Now answer the following question using the context provided.
        """),
            ("human", "Context:\n{context}\n\nQuestion: {question}"),
        ])

        def format_docs(docs):
            return "\n\n".join(d.page_content for d in docs)

        self.qa_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )

    def query(self, question: str):
        try:
            if not self.qa_chain:
                return {"answer": "System not initialized. Please load documents first.", "sources": []}

            if self.llm:
                # Generative mode
                answer = self.qa_chain.invoke(question)
                return {"answer": answer, "sources": []}
            else:
                # Retrieval-only mode
                docs = self.qa_chain.invoke(question)
                context = "\n\n".join([d.page_content for d in docs[:2]])
                return {
                    "answer": f"Based on the document:\n\n{context}",
                    "sources": [d.page_content[:200] for d in docs],
                }
        except Exception as e:
            print(f"❌ Error in query: {e}")
            traceback.print_exc()
            return {"answer": f"Internal error: {str(e)}", "sources": []}

    def load_from_text(self, text: str, source="memory"):
        doc = Document(page_content=text, metadata={"source": source})
        return self.create_vector_store([doc])


# Singleton
_rag_engine = None

def get_rag_engine():
    global _rag_engine
    if _rag_engine is None:
        _rag_engine = RAGEngine()
    return _rag_engine



from langchain.tools import tool
from datetime import datetime, timedelta

@tool
def calculate_annual_leave(join_date: str, current_date: str, enjoyed_leave: int) -> str:
    """Calculate annual leave balance based on join date, current date, and enjoyed leave.
    Args:
        join_date: Join date in format YYYY-MM-DD
        current_date: Current date in format YYYY-MM-DD
        enjoyed_leave: Number of annual leave days already enjoyed
    Returns:
        Remaining annual leave balance
    """
    # গণনার সূত্র: Labour Act অনুযায়ী ১৮ দিন কাজে ১ দিন লিভ
    start = datetime.strptime(join_date, "%Y-%m-%d")
    end = datetime.strptime(current_date, "%Y-%m-%d")
    total_days = (end - start).days
    # শুধু কাজের দিন? আমরা ধরে নিচ্ছি সব দিন কাজ করেছে (সাপ্তাহিক ছুটি বাদ দেওয়া জটিল)
    # সরলীকৃত: total_days কে ১৮ দিয়ে ভাগ
    earned_leave = total_days // 18
    balance = earned_leave - enjoyed_leave
    return f"Total days worked: {total_days}, earned leave: {earned_leave}, enjoyed: {enjoyed_leave}, balance: {balance} days."