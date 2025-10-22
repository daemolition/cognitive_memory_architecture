from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from datetime import datetime
import os

class LtMemory:
    def __init__(self, folder: str = "ltmemory_lc"):
        self.folder = folder
        os.makedirs(folder, exist_ok=True)

        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        try:
            self.vectorstore = FAISS.load_local(
                folder,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
        except Exception:
            self.vectorstore = None

    def create_document(self, message: str, session_id: str, role: str = "human") -> Document:
        return Document(
            page_content=message,
            metadata={
                "session_id": session_id,
                "role": role,
                "created_at": datetime.now().isoformat()
            }
        )

    def add_message(self, message: str, session_id: str, role: str = "human"):
        doc = self.create_document(message, session_id, role)

        if self.vectorstore:
            self.vectorstore.add_documents([doc])
        else:
            self.vectorstore = FAISS.from_documents([doc], self.embeddings)

        self.vectorstore.save_local(self.folder)


    def search(self, query: str, k: int = 3):
        """Ähnlichkeitssuche"""
        results = self.vectorstore.similarity_search(query, k=k)
        return [
            {
                "message": doc.page_content,
                "session_id": doc.metadata.get("session_id"),
                "role": doc.metadata.get("role"),
                "created_at": doc.metadata.get("created_at")
            }
            for doc in results
        ]
