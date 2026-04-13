import json
import os
from http.server import BaseHTTPRequestHandler
from typing import Dict

from langchain_community.vectorstores import FAISS
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter


# ---------------------------
# In-memory session history
# ---------------------------
STORE: Dict[str, BaseChatMessageHistory] = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in STORE:
        STORE[session_id] = InMemoryChatMessageHistory()
    return STORE[session_id]


# ---------------------------
# Small clinic knowledge base
# Based on the professor's notebook structure
# ---------------------------
RAW_DOCS = [
    "The clinic is specialized in sterilization and castration for dogs and cats. It does not provide routine general consultations or emergency care.",
    "Before sterilisation surgery, pets should fast for 8 to 12 hours. Water is allowed until 1 to 2 hours before surgery.",
    "Dogs cannot be sterilized while in heat. They should wait around two months after the end of heat before surgery.",
    "For animals older than 6 years, a preoperative blood test is mandatory because anesthetic risk increases with age.",
    "Pick-up time is approximately 12:00 for dogs and 15:00 for cats.",
    "If there is active bleeding, pale gums, or the animal does not respond after the operation, the clinic should be contacted immediately or an emergency veterinary service should be used.",
]


def build_retriever():
    documents = [Document(page_content=text) for text in RAW_DOCS]
    splitter = CharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=30,
        separator="\n",
    )
    split_docs = splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(split_docs, embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": 3})


RETRIEVER = build_retriever()


# ---------------------------
# Chat chain (system prompt + memory + RAG)
# ---------------------------
def build_chain():
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                (
                    "You are a helpful assistant for a veterinary clinic. "
                    "Answer briefly and professionally in the same language as the user. "
                    "Use the provided clinic context when it is relevant. "
                    "If the context does not contain the answer, say so clearly and answer conservatively. "
                    "Do not diagnose. Focus on sterilization, castration, preparation, timing, and clinic logistics."
                ),
            ),
            MessagesPlaceholder(variable_name="history"),
            (
                "human",
                "Clinic context:\n{context}\n\nUser question: {input}",
            ),
        ]
    )

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
    chain = prompt | llm

    return RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history",
    )


CHAT_CHAIN = build_chain()


class handler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, payload: dict) -> None:
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode("utf-8"))

    def do_OPTIONS(self) -> None:
        self._send_json(200, {"ok": True})

    def do_POST(self) -> None:
        if not os.environ.get("OPENAI_API_KEY"):
            self._send_json(500, {"error": "OPENAI_API_KEY is not configured"})
            return

        try:
            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_length)
            data = json.loads(raw_body or "{}")
        except Exception:
            self._send_json(400, {"error": "Invalid JSON body"})
            return

        message = (data.get("message") or "").strip()
        session_id = (data.get("session_id") or "default").strip()

        if not message:
            self._send_json(400, {"error": "message must not be empty"})
            return

        try:
            retrieved_docs = RETRIEVER.invoke(message)
            context = "\n\n".join(doc.page_content for doc in retrieved_docs)

            response = CHAT_CHAIN.invoke(
                {
                    "input": message,
                    "context": context,
                },
                config={"configurable": {"session_id": session_id}},
            )

            reply = response.content if hasattr(response, "content") else str(response)

            self._send_json(
                200,
                {
                    "response": reply,
                    "session_id": session_id,
                    "context_used": context,
                },
            )
        except Exception as exc:
            self._send_json(500, {"error": f"Chat request failed: {exc}"})

            