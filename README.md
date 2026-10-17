# PolyBot: AI Student Handbook & Campus Assistant
**Talibon Polytechnic College (TPC)**  
*IS Professional Elective #4 - Generative AI Capstone Project*

PolyBot is an enterprise-grade Retrieval-Augmented Generation (RAG) assistant specifically designed for Talibon Polytechnic College. It provides students, faculty, and campus visitors with instant, grounded answers regarding academic policies, grading schemes, uniform regulations, and student affairs based strictly on the official **TPC Student Handbook v.04**.

---

## 🏛️ System Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                        POLYBOT RAG ARCHITECTURE                        │
│                                                                        │
│   [ 203-pg Handbook PDF ] ──> [ 150-Word Chunker ] ──> [ ChromaDB ]    │
│                                (25-word overlap)       (Cosine Sim)    │
│                                                             │          │
│                                                             ▼          │
│   [ Streamlit Web App ] <── [ Gemini 3.8 Flash ] <── [ RAG Engine ]    │
│       (Gemini-styled UI)         (Temp 0.0)             (Top-5 Chunks) │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start (Local Run)

### 1. Prerequisites
- Python 3.10+
- Valid `GEMINI_API_KEY` stored in `.env`

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Web Interface
```bash
streamlit run app.py
```
PolyBot will open automatically in your browser at `http://localhost:8501`.

---

## 🐳 Docker Deployment (Deliverable 17)

PolyBot includes an optimized multi-stage Docker build for minimal container size and isolated runtime dependencies:

```bash
# 1. Build the Docker image
docker build -t polybot-tpc:latest .

# 2. Run the container
docker run -d -p 8501:8501 --env-file .env --name polybot-container polybot-tpc:latest
```
Access the application at `http://localhost:8501`.

---

## 🌐 Public Cloud Deployment (Deliverable 18)

### Option 1: Streamlit Community Cloud (Recommended & Free)
1. Push this repository to GitHub.
2. Sign in to [share.streamlit.io](https://share.streamlit.io).
3. Select your `polybot-capstone` repo and set the main file to `app.py`.
4. In **Advanced Settings > Secrets**, paste your key:
   ```toml
   GEMINI_API_KEY = "your_actual_key_here"
   ```
5. Click **Deploy!** Your app will be live at `https://<your-app-name>.streamlit.app`.

### Option 2: Render.com / Hugging Face Spaces (Docker)
1. Connect your repository to Render or Hugging Face.
2. Select **Docker Runtime** (it will automatically use the `Dockerfile`).
3. Set the environment variable `GEMINI_API_KEY`.

---

## 👥 Team Roles & Responsibilities

- **Jerwin Villarin**: QA, Evaluation & Dataset Curation (TPC Handbook & Website ground truth)
- **Trisha Marie Udtohan**: Lead Developer (Backend, Ingestion Pipeline & ChromaDB Indexing)
- **Jenalyn Sabal**: AI Orchestrator (RAG Orchestration, Guardrails, Memory & Gemini API)
- **Kaycee Cerida**: DevOps, Web Interface (Streamlit) & Cloud Deployment
