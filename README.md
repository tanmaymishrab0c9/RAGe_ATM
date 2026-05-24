# RAGe Against The Machine 
 
> A full-stack Retrieval-Augmented Generation (RAG) application — upload PDFs, store semantic embeddings in PostgreSQL + pgvector, and ask AI-powered questions grounded in your documents using the Gemini API.
 
---
 
## Features
 
- **PDF Upload & Ingestion** — Drag-and-drop PDF processing pipeline
- **Recursive Text Chunking** — Semantically-aware splitting with LangChain
- **Semantic Vector Search** — Nearest-neighbor retrieval via pgvector
- **PostgreSQL + pgvector Integration** — Production-grade vector storage
- **Metadata Tracking** — Document name, page number, and chunk index per embedding
- **Gemini-powered Responses** — Context-grounded AI answers via Gemini API
- **Full-stack Architecture** — Next.js frontend + FastAPI backend
- **Dockerized Database** — One-command PostgreSQL + pgvector setup
- **Real-time Context Retrieval** — Live similarity search on every query
---
 
## Tech Stack
 
| Layer | Technology |
|-------|-----------|
| **Frontend** | Next.js, React, Tailwind CSS |
| **Backend** | FastAPI, SQLAlchemy |
| **Database** | PostgreSQL, pgvector |
| **Embeddings** | Sentence Transformers |
| **PDF Parsing** | PyMuPDF |
| **Chunking** | LangChain `RecursiveCharacterTextSplitter` |
| **AI Generation** | Gemini API |
 
---
 
## Architecture
 
```
Next.js Frontend
      │
      ▼
FastAPI Backend
      │
      ▼
Sentence Embeddings (SentenceTransformer)
      │
      ▼
PostgreSQL + pgvector
      │
      ▼
Semantic Retrieval (cosine similarity search)
      │
      ▼
Gemini API → Response returned to Frontend
```
 
---
 
## Project Structure
 
```
RAGE_ATM/
│
├── rage_backend/
│   ├── main.py          # FastAPI app & route definitions
│   ├── database.py      # SQLAlchemy engine & session setup
│   ├── models.py        # ORM models (document chunks + embeddings)
│   ├── schemas.py       # Pydantic request/response schemas
│   ├── utils.py         # PDF parsing, chunking, embedding helpers
│   └── .env             # Environment variables (API keys, DB URL)
│
├── rage_frontend/
│   ├── app/             # Next.js App Router pages & components
│   ├── public/          # Static assets
│   ├── package.json
│   └── next.config.ts
│
└── README.md
```
 
---
 
## How It Works
 
1. **User uploads a PDF** via the Next.js frontend
2. **Backend extracts text** using PyMuPDF, page by page
3. **Recursive chunking** splits text into semantically coherent pieces (paragraphs → sentences → words → characters) with overlap for contextual continuity
4. **SentenceTransformer generates vector embeddings** for each chunk
5. **Embeddings stored** in PostgreSQL with pgvector, alongside metadata (doc name, page, chunk index)
6. **User asks a question** through the chat interface
7. **Query embedding generated** using the same SentenceTransformer model
8. **Vector similarity search** retrieves the most relevant chunks from the database
9. **Retrieved context injected** into a structured Gemini prompt
10. **AI-generated answer** streamed back to the frontend
---
 
## Recursive Chunking
 
The application uses `RecursiveCharacterTextSplitter` from LangChain to preserve semantic structure. The splitter cascades through a hierarchy of separators:
 
```
Paragraphs  →  Sentences  →  Words  →  Characters
```
 
Chunk overlap is configured to ensure contextual continuity at boundaries, reducing information loss during retrieval.
 
---
 
## API Endpoints
 
### `POST /upload-pdf`
 
Uploads and ingests a PDF into the vector database.
 
**Request:** `multipart/form-data` with a PDF file field.
 
**Response:**
```json
{
  "message": "PDF ingested successfully",
  "chunks_stored": 42
}
```
 
---
 
### `POST /ask`
 
Runs a semantic search over stored embeddings and returns a Gemini-generated answer grounded in the retrieved context.
 
**Request:**
```json
{
  "question": "What is recursive chunking?"
}
```
 
**Response:**
```json
{
  "answer": "Recursive chunking is a text splitting strategy that...",
  "sources": [
    { "document": "paper.pdf", "page": 3, "chunk_index": 7 }
  ]
}
```
 
---
 
## Getting Started
 
### Prerequisites
 
- Docker & Docker Compose
- Python 3.10+
- Node.js 18+
- A [Gemini API key](https://aistudio.google.com/app/apikey)
### 1. Start the Database
 
```bash
docker compose up -d
```
 
This spins up PostgreSQL with the pgvector extension enabled.
 
### 2. Configure Environment
 
Create `rage_backend/.env`:
 
```env
DATABASE_URL=postgresql://user:password@localhost:5432/rage_db
GEMINI_API_KEY=your_gemini_api_key_here
```
 
### 3. Run the Backend
 
```bash
cd rage_backend
pip install -r requirements.txt
uvicorn main:app --reload
```
 
Backend will be available at `http://localhost:8000`.
 
### 4. Run the Frontend
 
```bash
cd rage_frontend
npm install
npm run dev
```
 
Frontend will be available at `http://localhost:3000`.
 
---
 
## Environment Variables
 
| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string |
| `GEMINI_API_KEY` | Google Gemini API key |
 
---
