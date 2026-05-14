# 📚 Studyeasy AI

An AI-powered study assistant that allows students to upload PDFs/notes and ask questions directly from their study material using Retrieval-Augmented Generation (RAG).

The application uses:

* FastAPI backend
* Streamlit frontend
* ChromaDB vector storage
* Groq LLMs
* Embedding API
* Session-based retrieval architecture

---

# 🚀 Features

## 📄 PDF Uploads

Students can upload PDF notes, assignments, lecture slides, and study material.

## 💬 Chat With Notes

Ask contextual questions directly from uploaded study material.

## 🧠 RAG Architecture

Uses Retrieval-Augmented Generation for grounded responses.

## 📌 Citations

Answers include document citations and page references.

## 📝 Summaries

Optional concise summaries for revision.

## 🔒 Session Isolation

Each uploaded PDF gets its own temporary vector collection.

## 🧹 Automatic Cleanup

Expired sessions and vector collections are automatically deleted.

## ☁️ Cloud Deployment

* Backend deployed on Render
* Frontend deployed on Streamlit Cloud

---

# 🏗️ Architecture

```text
Streamlit Frontend
        ↓
FastAPI Backend
        ↓
Embedding API(Jina)
        ↓
ChromaDB Vector Store
        ↓
Groq LLM
```

---

# 🛠️ Tech Stack

## Frontend

* Streamlit

## Backend

* FastAPI
* Uvicorn

## AI / ML

* Groq LLM
* ChromaDB
* LangChain
* Embedding API (Jina)

## PDF Processing

* PyMuPDF

---

# 📂 Project Structure

```text
project/
│
├── uploads/
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── embeddings.py
│   ├── pipeline.py
│   ├── prompts.py
│   ├── search.py
│   ├── session_manager.py
│   └── vectorstore.py
│
├── data/
│   └── vector_store/
│
├── app.py
├── main.py
├── requirements.txt
├── runtime.txt
├── .env
└── README.md
```

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone <your-repo-url>
cd <repo-name>
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
JINA_API_KEY=your_embedding_api_key
BACKEND_URL=http://127.0.0.1:8000
```

---

# ▶️ Running The Backend

```bash
uvicorn main:app --reload
```

Backend runs on:

```text
http://127.0.0.1:8000
```

Swagger Docs:

```text
http://127.0.0.1:8000/docs
```

---

# ▶️ Running The Frontend

```bash
streamlit run app.py
```

---

# 📡 API Endpoints

## Upload PDF

```http
POST /upload
```

Uploads PDF and creates a session.

### Response

```json
{
  "message": "PDF uploaded successfully",
  "session_id": "session_xxxxx"
}
```

---

## Chat With PDF

```http
POST /chat
```

### Request

```json
{
  "question": "What is polymorphism?",
  "session_id": "session_xxxxx",
  "top_k": 8,
  "min_score": 0.2,
  "summarize": true
}
```

---

# 🌐 Deployment

## Backend

Deployed on Render.

## Frontend

Deployed on Streamlit Community Cloud.

---

# 🔮 Potential Improvements


* Viva questions generation
* Formula extraction
* Better retrieval ranking
* Authentication
* Multi-file support
* Streaming responses

---



# 👨‍💻 Author

Garv Kaushik

Engineering Student | ML & Web Development Enthusiast
