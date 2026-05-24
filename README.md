# RAGe Against The Machine

A full-stack Retrieval-Augmented Generation (RAG) application that allows users to upload PDFs, store semantic embeddings in PostgreSQL + pgvector, and ask AI-powered questions grounded in document context using Gemini API.

---

# Features

- PDF Upload & Ingestion
- Recursive Text Chunking
- Semantic Vector Search
- PostgreSQL + pgvector Integration
- Metadata Tracking (document name, page number, chunk index)
- Gemini-powered AI Responses
- Full-stack Frontend + Backend Architecture
- Dockerized PostgreSQL Database
- Real-time Context Retrieval

---

# Tech Stack

## Frontend
- Next.js
- React
- Tailwind CSS

## Backend
- FastAPI
- SQLAlchemy
- PostgreSQL
- pgvector
- PyMuPDF
- Sentence Transformers
- LangChain Text Splitters
- Gemini API

---

# Architecture

```text
Next.js Frontend
        ↓
FastAPI Backend
        ↓
Sentence Embeddings
        ↓
PostgreSQL + pgvector
        ↓
Semantic Retrieval
        ↓
Gemini API Response Generation
