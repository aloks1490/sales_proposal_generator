import streamlit as st

from langchain_community.llms import Ollama
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser

from langchain_core.prompts import PromptTemplate


class ProposalRAG:
    def __init__(self):
        # Fast, stable embedding model
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        # Local LLM via Ollama
        self.llm = Ollama(model="granite4:1b")

        self.vector_db = None
        self.rag_chain = None

    def process_documents(self, documents):
        """Chunk → Embed → Store documents"""

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )

        splits = text_splitter.split_documents(documents)

        self.vector_db = Chroma.from_documents(
            documents=splits,
            embedding=self.embeddings,
            persist_directory="./data/chroma_db"
        )

        return self.vector_db

    def _build_rag_chain(self):
        """Stable LCEL RAG pipeline"""

        prompt = ChatPromptTemplate.from_template(
            """
You are an expert sales proposal writer.

Use the following internal context and meeting notes
to draft a professional, client-ready proposal.

CONTEXT FROM COMPANY FILES:
{context}

MEETING NOTES / CLIENT NEEDS:
{meeting_text}

USER INSTRUCTIONS:
{question}

Write the proposal in **Markdown** using this structure:

# Proposal
## 1. Executive Summary
## 2. Understanding Your Needs
## 3. Proposed Solution
## 4. Pricing & Packages
## 5. Next Steps
"""
        )

        retriever = self.vector_db.as_retriever(search_kwargs={"k": 4})

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        extract_question = RunnableLambda(lambda x: x["question"])
        extract_meeting = RunnableLambda(lambda x: x["meeting_text"])
        format_context = RunnableLambda(format_docs)

        self.rag_chain = (
            {
                "context": extract_question | retriever | format_context,
                "question": extract_question,
                "meeting_text": extract_meeting,
            }
            | prompt
            | self.llm
            | StrOutputParser()
        )

    def generate_proposal(self, user_prompt, meeting_text):
        """Run RAG pipeline"""

        if self.vector_db is None:
            raise RuntimeError("Call process_documents() before generating a proposal.")

        if self.rag_chain is None:
            self._build_rag_chain()

        return self.rag_chain.invoke(
            {
                "question": user_prompt,
                "meeting_text": meeting_text,
            }
        )
