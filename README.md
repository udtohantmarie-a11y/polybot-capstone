# PolyBot: TPC AI Student Handbook & Campus Assistant
**Talibon Polytechnic College (TPC)**  
*IS Professional Elective #4 - Generative AI Capstone Project*  
**Team Members:** Jerwin Villarin, Trisha Marie Udtohan, Jenalyn Sabal, Kaycee Cerida  

PolyBot is an enterprise-grade Retrieval-Augmented Generation (RAG) web application specifically engineered for Talibon Polytechnic College. It assists students, faculty, and visitors with inquiries regarding academic policies, grading schemes, uniform regulations, dropping procedures, and student conduct, strictly grounded in the official **TPC Student Handbook v.04**.

* **🌐 Live Deployed App**: `https://polybot-capstone-production.up.railway.app` (Runs publicly on Railway via Docker, no login required)
* **📄 Knowledge Source**: Official TPC Student Handbook v.04 (203 pages, extracted and segmented into 268 discrete chunks) and Official TPC Website Compilation.
* **⚠️ API Usage & Rate Limits**: PolyBot utilizes Google Gemini 3.8 Flash on a free-tier API plan (15 requests/minute, 1,000,000 tokens/minute). If multiple requests are sent rapidly, brief rate-limiting pauses may occur.

---

## 📚 Gabay sa mga Ginamit na Teknolohiya at Bakit Sila Ginamit (Tech Stack Guide)

Itong seksyon na ito ay ginawa upang maging pamilyar ang buong grupo sa bawat bahagi ng system para sa darating na Final Defense at Technical Report.

### 1. Frontend & Web Interface: **Streamlit**
* **Ano ito:** Isang Python-based open-source framework para sa paggawa ng interactive web applications.
* **Bakit ito ginamit:**
  - **Python-Native:** Direktang nakakausap ang ating backend (ChromaDB at Gemini API) nang hindi na kailangang gumawa ng hiwalay na React/Vue/Node.js frontend.
  - **Gemini-Like Chat UI:** May built-in support para sa modern chat bubbles (`st.chat_message`), input bar (`st.chat_input`), at live typewriter streaming effect (`st.write_stream` o token streaming).
  - **Conversational Memory:** Gamit ang `st.session_state`, nagawa natin ang chat history sa kaliwang sidebar kung saan pwedeng balikan ang mga dating tanong at magsimula ng bagong chat (katulad na katulad ng Google Gemini at ChatGPT).

### 2. LLM Engine: **Google Gemini 3.8 Flash (`google-genai` SDK)**
* **Ano ito:** Ang pinakabagong high-efficiency generative AI model mula sa Google DeepMind.
* **Bakit ito ginamit:**
  - **Mabilis at Matipid sa Latency:** Ang `flash` variant ay dinisenyo para sa real-time conversations na may sub-second token generation.
  - **Multilingual Support (Bisaya, Tagalog, English):** Likas na nakakaintindi at nakakapagsalita ang Gemini ng Bisaya (Cebuano) at Tagalog. Kahit Ingles ang nakasulat sa Handbook, kapag nagtanong ang estudyante sa Bisaya, sasagutin ito ni PolyBot sa natural at tamang Bisaya habang pinapanatili ang opisyal na terms ng TPC.
  - **Temperature 0.0 (Anti-Hallucination):** Itinakda natin ang temperature sa eksaktong `0.0`. Ibig sabihin, greedy at deterministic ang AI—hindi ito magiging "creative" o mag-iimbento ng mga patakaran. Kung wala sa handbook, susundin nito ang guardrail at aamining wala itong sapat na impormasyon.

### 3. Vector Database: **ChromaDB**
* **Ano ito:** Isang open-source, embedded vector database na ginagamit sa pag-iimbak at mabilisang paghahanap ng high-dimensional vector embeddings.
* **Bakit ito ginamit:**
  - **Serverless at Embedded:** Tumatakbo ito nang lokal sa loob ng ating project folder (`data/chroma_db`) nang hindi nangangailangan ng hiwalay na mamahaling external cloud database tulad ng Pinecone o Milvus.
  - **Sub-50ms Retrieval:** Mabilis nitong nahahanap ang top-5 pinaka-kaugnay na handbook chunks mula sa 268 chunks ng TPC Handbook.
  - **Cosine Similarity:** Sinusukat nito ang anggulo (direction) ng semantic meaning sa pagitan ng tanong ng user at ng talata sa handbook, anuman ang haba ng tanong.

### 4. Embedding Model: **Hugging Face (`sentence-transformers/all-MiniLM-L6-v2`)**
* **Ano ito:** Isang neural network model na nagta-transform ng text papuntang 384-dimensional dense vectors.
* **Bakit ito ginamit:**
  - **Magaan at Mabisa:** May sukat lamang na ~80 MB, kaya napakabilis nitong mag-embed ng mga salita nang hindi bumibigat ang RAM ng ating server.
  - **Cross-Lingual Semantic Capability:** Kahit nakasulat sa Tagalog o Bisaya ang tanong, nakikilala pa rin nito ang konseptong katumbas sa English text ng handbook (halimbawa: "grado" -> "grades", "gupit" -> "haircut").

### 5. Backend Deep Learning Framework: **PyTorch (CPU-Only Build)**
* **Ano ito:** Ang engine na nagpapatakbo sa Hugging Face embedding model.
* **Bakit CPU build ang ginamit:**
  - Ang standard PyTorch ay may kasamang GPU/CUDA drivers na umaabot sa 2.5 GB. Dahil CPU-only server ang ginagamit natin sa Railway, ang CPU build (~150 MB lang) ang pinili para mabilis ang build at hindi ma-ubos ang memory limit sa cloud.

### 6. Containerization: **Docker (Multi-Stage Build)**
* **Ano ito:** Isang teknolohiya na nagbabalot sa buong application (code, Python packages, at database) sa isang standardized lightweight container.
* **Bakit Multi-Stage ang ginamit (Deliverable 17):**
  - **Stage 1 (Builder):** Dito ini-install ang mga compiler at pip packages.
  - **Stage 2 (Runtime):** Kinokopya lang ang mga kailangang files papunta sa malinis at magaan na `python:3.11-slim` base image.
  - **Resulta:** Maliit ang image size, mas secure, at walang extraneous build tools sa production.

### 7. Cloud Deployment Platform: **Railway**
* **Ano ito:** Isang modernong cloud Infrastructure-as-a-Service (IaaS/PaaS) platform.
* **Bakit ito ginamit (Deliverable 18):**
  - **Direktang GitHub Integration:** Sa bawat git commit, awtomatiko nitong binabasa ang ating `Dockerfile` at muling dine-deploy ang website.
  - **Public Live URL:** Nagbibigay ito ng HTTPS domain (e.g. `https://polybot-capstone-production.up.railway.app`) na ma-a-access ng panel kahit saan gamit ang browser o cellphone.
  - **Dynamic Port Routing:** Gumagana ito sa port `8080` (o `$PORT`), kung saan awtomatikong itinuturo ng Railway ang web traffic papunta sa ating Streamlit UI.

### 8. Secrets Management: **`python-dotenv`**
* **Ano ito:** Library na nagbabasa ng environment variables mula sa `.env` file.
* **Bakit ito ginamit:**
  - Pinipigilan nito ang pag-hardcode ng `GEMINI_API_KEY` sa loob ng Python code.
  - Naka-ignore ang `.env` sa ating `.gitignore` upang hindi ma-leak sa public GitHub ang ating secret credentials.

---

## 🏛️ End-to-End System Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                        POLYBOT RAG PIPELINE                            │
│                                                                        │
│   [ 203-pg Handbook PDF ] ──> [ 150-Word Chunker ] ──> [ ChromaDB ]    │
│   (Official TPC Source)        (25-word overlap)       (268 Chunks)    │
│                                                             │          │
│                                                             ▼          │
│   [ Streamlit Web App ] <── [ Gemini 3.8 Flash ] <── [ RAG Engine ]    │
│   • Multilingual (Bisaya/    • Temp 0.0 (Strict)     • Cosine Search   │
│     Tagalog/English)         • Citations Included    • Top-5 Chunks    │
│   • Sidebar Chat History     • Streaming Tokens                        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Step-by-Step Lifecycle ng Bawat Tanong (Query Lifecycle)

Kapag nag-type ang isang estudyante sa website:
1. **Pagtanggap sa Input:** Tinatanggap ng Streamlit ang tanong ng user (hal. *"Unsa ang passing grade sa TPC?"*).
2. **Dense Vector Embedding:** Ginagawang 384-dimensional number vector ng `all-MiniLM-L6-v2` ang tanong.
3. **Similarity Search:** Hinahanap ng ChromaDB ang top-5 chunks sa database na may pinakamataas na Cosine Similarity score kaugnay sa tanong.
4. **Context & History Injection:** Pinagsasama ang 5 handbook chunks, ang nakaraang 2–3 turns ng conversation (conversational memory), at ang tanong ng user sa loob ng isang formatted prompt.
5. **Deterministic Inference:** Ipinapadala ito sa Gemini 3.8 Flash na may Temperature 0.0 at mahigpit na system guardrails.
6. **Language Adaptation:** Nadedetect ng Gemini na Bisaya ang tanong, kaya isinasalin at binubuo nito ang sagot sa natural na Bisaya habang pinapanatili ang opisyal na mga numero at Articles.
7. **Live UI Streaming & Verification:** Lumalabas ang sagot nang patayp-type sa screen, kasama ang expandable **"📖 Verified Sources"** drawer na nagpapakita ng eksaktong handbook chunks na pinagkunan.

---

## 🚀 Paano Patakbuhin Locally

```powershell
# 1. Kopyahin ang .env.example papuntang .env at ilagay ang iyong Gemini API Key
copy .env.example .env

# 2. Siguraduhing installed ang dependencies
pip install -r requirements.txt

# 3. Patakbuhin ang Streamlit web app
python -m streamlit run app.py
```
Buksan sa browser: `http://localhost:8501`

---

## 🐳 Docker Run (Lokal na Container)

```bash
docker build -t polybot-tpc:latest .
docker run -p 8080:8080 --env-file .env polybot-tpc:latest
```
Buksan sa browser: `http://localhost:8080`

---

## 👥 Responsibilidad ng Bawat Miyembro

- **Jerwin Villarin**: QA, Evaluation & Dataset Curation (Paglilinis ng Handbook PDF at Website data, paggawa ng 5 realistic + 1 refusal demo queries).
- **Trisha Marie Udtohan**: Lead Developer (Backend Ingestion pipeline, chunking strategy, ChromaDB persistent vector storage, Cosine Similarity metric).
- **Jenalyn Sabal**: AI Orchestrator (RAG Orchestration, Gemini API integration, prompt guardrails, temperature 0.0, at multilingual configuration).
- **Kaycee Cerida**: DevOps, UI & Deployment Lead (Streamlit Web UI, Gemini-style chat history, Dockerfile multi-stage containerization, at Railway live deployment).
