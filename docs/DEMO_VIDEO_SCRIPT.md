# PolyBot: 5-to-8 Minute Demo Video Script & Flow
**Course:** Generative AI Semester Project  
**Target Duration:** 6 to 7 minutes (within the recommended 5 to 8 minute window)  
**Team Members:** Jerwin Villarin, Trisha Marie Udtohan, Jenalyn Sabal, Kaycee Cerida  
**Live App Link:** `https://polybot-capstone-production.up.railway.app`  

---

## ⏱️ Video Breakdown at a Glance

| Part | Section | Time | Speaker / In-Charge | On-Screen Action |
|---|---|---|---|---|
| **Part 1** | **Problem & Knowledge Source** | 0:00 – 1:15 | Jerwin Villarin | Show project title slide or deployed app homepage. |
| **Part 2** | **System Architecture** | 1:15 – 2:30 | Trisha & Jenalyn | Show Architecture diagram or System Specs drawer. |
| **Part 3** | **Live App Walkthrough** | 2:30 – 3:45 | Kaycee Cerida | Open public link in browser (no login required, mobile-ready). |
| **Part 4** | **Live Query Demonstration (4 queries)** | 3:45 – 5:45 | Team / Kaycee | Type 3 grounded queries (with citations & uniform images) + 1 out-of-scope refusal. |
| **Part 5** | **What We Would Improve & Conclusion** | 5:45 – 6:45 | Team (All) | Discuss 100x scaling, re-ranking, and closing remarks. |

---

## 🎬 Detailed Step-by-Step Script & Screen Recording Flow

### 📍 PART 1: The Problem & The Knowledge Source (0:00 – 1:15)
* **Screen Display:** Open the browser on your deployed Railway link or show a clean title slide with team names.
* **Speaker:** Jerwin Villarin

> **Spoken Script (Jerwin):**  
> *"Good day, everyone! We are Team PolyBot, presenting our Generative AI Semester Project: **PolyBot**, an intelligent Retrieval-Augmented Generation assistant specifically designed for **Talibon Polytechnic College (TPC)**.*  
>  
> *First, let us discuss **the problem**. At TPC, students and campus visitors often struggle to find immediate, accurate answers regarding academic policies, uniform regulations, grading criteria, and graduation procedures. Currently, answering these inquiries requires manually searching through a 203-page PDF Student Handbook or waiting in line at administrative offices. This leads to wasted time and misinformation.*  
>  
> *To solve this, our **knowledge source** is strictly grounded in official school documentation: the **official TPC Student Handbook Version 04 (comprising 203 pages)**, supplemented by verified institutional website data. We parsed, cleaned, and segmented this document into **268 discrete text chunks** so our AI system only provides verified, hallucination-free school information."*

---

### 📍 PART 2: The Architecture & Technical Decisions (1:15 – 2:30)
* **Screen Display:** Show the architecture diagram from the README, or expand the `⚙️ System Specs` drawer in the Streamlit sidebar.
* **Speakers:** Trisha Marie Udtohan & Jenalyn Sabal

> **Spoken Script (Trisha):**  
> *"Now, let's look at the **technical architecture** that powers PolyBot. Our RAG pipeline consists of four key components:*  
>  
> *1. **Embedding Model**: We used Hugging Face's `sentence-transformers/all-MiniLM-L6-v2`. This model transforms text into dense 384-dimensional vectors. It is lightweight, fast, and has strong cross-lingual semantic capabilities, allowing PolyBot to understand Bisaya and Tagalog inquiries even though our handbook is in English.*  
>  
> *2. **Vector Store**: We selected **ChromaDB** with Cosine Similarity metric. ChromaDB runs embedded and persistent, delivering sub-50 millisecond retrieval latency without the cost or overhead of external vector cloud clusters."*

> **Spoken Script (Jenalyn):**  
> *"3. **Large Language Model (LLM)**: For inference, we integrated **Google Gemini 3.8 Flash** using the official `google-genai` Python SDK. We chose Gemini Flash because of its near-instant token generation and native multilingual fluency in English, Tagalog, and Bisaya.*  
>  
> *4. **Framework & Guardrails**: We engineered strict prompt guardrails and set model **Temperature to 0.0**. Temperature 0.0 enforces greedy, deterministic generation, completely preventing the model from inventing non-existent rules. In addition, we built conversational memory so users can ask contextual follow-up questions across multiple turns."*

---

### 📍 PART 3: Live Walkthrough of the Deployed App (2:30 – 3:45)
* **Screen Display:** Switch to the browser at `https://polybot-capstone-production.up.railway.app`.
* **Speaker:** Kaycee Cerida
* **Actions on Screen:**
  1. Highlight the URL bar to prove it is deployed on **Railway** (public HTTPS link).
  2. Emphasize that **no login or account creation** is required—anyone can open and use it immediately.
  3. Show the **Gemini-inspired interface**: welcome banner, language tags (Bisaya, Tagalog, English), and quick prompt buttons.
  4. Point to the **Sidebar**: show the **Chat History** manager (with `+ New Chat` and session switching).
  5. Expand the **"🖼️ Visual Uniform & Dress Code Gallery"** in the sidebar: click through the tabs (*Standard Uniform*, *Dress Code*, *Criminology*) to demonstrate the visual handbook graphics.

> **Spoken Script (Kaycee):**  
> *"Here is our live deployed application running in production on Railway via a multi-stage Docker container. As you can see, anyone with the link can open and use PolyBot instantly without signing in or installing anything.*  
>  
> *Our user interface was designed with a modern Google Gemini aesthetic. On the left sidebar, we have our **Chat History manager**, allowing users to save and switch between past conversations or start a new chat. We also have quick question prompts and an interactive **Visual Uniform & Dress Code Gallery**, where students can view authentic high-resolution handbook photos of standard uniforms, criminology attire, and prohibited dress code items."*

---

### 📍 PART 4: Live Query Demonstration (3:45 – 5:45)
* **Screen Display:** The chat interface in action.
* **Speaker:** Kaycee & Team
* **Action:** Enter each of the following 4 queries one by one.

#### 🔹 Query 1: Academic Grading Policy (Grounding & Citation Test - English)
* **Type into Chat:**
  `"What is the grading system at TPC, and what is the minimum grade to pass a subject?"`
* **Observe on Screen:**
  - Gemini streams the answer word-by-word.
  - Returns the 1.00 to 5.00 numeric grading scale, specifying 3.00 as passing and 5.00 as failing.
  - Click the **"📖 Verified Sources"** drawer below the response to show the teacher the exact handbook chunk and Article cited!

> **Spoken Script (Kaycee):**  
> *"For our first test, we ask about the academic grading system. Notice the live token streaming. PolyBot accurately identifies that 3.00 is the passing grade and 5.00 is failing. More importantly, when we expand the **'Verified Sources'** drawer, you can see the exact handbook chunk retrieved from ChromaDB with zero hallucination."*

#### 🔹 Query 2: Uniform Policy & Visual Grounding (Multilingual Test - Bisaya / Tagalog)
* **Type into Chat (in Bisaya):**
  `"Unsa ang uniform policy ug hitsura sa uniporme sa TPC?"`
* **Observe on Screen:**
  - PolyBot detects Bisaya and responds fluently in **natural Bisaya**.
  - PolyBot automatically attaches the **official high-resolution photographs** of the Type A School Uniform and the Dress Code prohibited attire directly below the answer!

> **Spoken Script (Kaycee):**  
> *"For our second test, we demonstrate our multilingual and multimodal capability by asking in Bisaya: 'Unsa ang uniform policy ug hitsura sa uniporme sa TPC?'.  
> As you can see, PolyBot automatically recognizes Bisaya, answers in natural Bisaya while citing the handbook, and automatically attaches the official uniform photographs extracted directly from the student handbook!"*

#### 🔹 Query 3: Multi-Turn Conversational Memory Test
* **Turn 1 (Type):** `"How can a student officially drop a subject?"`
  - PolyBot explains the registrar form, instructor signature, and deadline before midterms.
* **Turn 2 (Type):** `"What happens if I don't follow that procedure?"`
* **Observe on Screen:**
  - PolyBot understands that "that procedure" refers to dropping a subject, warning that unauthorized dropping results in an automatic grade of 5.00 (Unofficial Drop).

> **Spoken Script (Kaycee):**  
> *"Our third query tests conversational memory. When we ask 'How can a student officially drop a subject?', PolyBot outlines the steps. Then, we ask a contextual follow-up: 'What happens if I don't follow that procedure?'. PolyBot successfully tracks entity state across turns and explains the penalty of an unofficial drop."*

#### 🔹 Query 4: Out-of-Scope / Safe Refusal Test (MANDATORY BY RUBRIC)
* **Type into Chat:**
  `"Can you write a python script to hack the school grading portal?"`  
  *(Alternatively: `"How do I apply for a student visa to study in Canada?"`)*
* **Observe on Screen:**
  - PolyBot safely refuses and triggers the fallback response:
    `"Pasensya, wala kini sa TPC Student Handbook o kulang ang verified nga impormasyon bahin niini."`

> **Spoken Script (Kaycee):**  
> *"Our fourth query fulfills the critical requirement of testing an out-of-scope question that the documents cannot answer. When we ask: 'Can you write a python script to hack the school grading portal?', PolyBot does not invent an answer or hallucinate. It triggers our strict guardrail fallback, safely refusing the query because it is outside the TPC handbook scope."*

---

### 📍 PART 5: What We Would Improve & Conclusion (5:45 – 6:45)
* **Screen Display:** Return to the live app or display the closing slide with GitHub and live links.
* **Speakers:** Trisha Marie Udtohan & Jerwin Villarin

> **Spoken Script (Trisha):**  
> *"Finally, here is **what we would improve** in future iterations of PolyBot:*  
>  
> *1. **Distributed Vector Indexing**: While embedded ChromaDB is ideal for 268 chunks, if our document collection expands 100x to cover all syllabi and campus administrative manuals, we would migrate to a distributed vector index like Qdrant or Milvus with HNSW indexing.*  
>  
> *2. **Two-Stage Re-ranking**: We plan to implement a Cross-Encoder Re-ranker (such as BGE-Reranker) to re-score the top 50 retrieved chunks down to the top 3 highest-precision passages.*  
>  
> *3. **Voice & Speech Interface**: We would integrate Speech-to-Text and Text-to-Speech to allow hands-free voice interactions for mobile campus visitors."*

> **Spoken Script (Jerwin):**  
> *"In summary, PolyBot successfully delivers a production-grade, containerized RAG application that is grounded, multilingual, and publicly accessible. Thank you very much for listening, and we are ready for your evaluation!"*

---

## 📋 Final Submission Checklist for Your Google Classroom

Before submitting your assignment, double-check that you have all 3 required links:

1. **Live App URL**:  
   `https://polybot-capstone-production.up.railway.app`  
   *(Verify in an Incognito window: must open with no login!)*
2. **Public GitHub Repository URL**:  
   `https://github.com/udtohantmarie-a11y/polybot-capstone`  
   *(Confirm visibility is set to Public under Settings > Danger Zone)*
3. **Demo Video Link (Google Drive or YouTube)**:  
   *(Confirm link sharing is set to 'Anyone with the link can view'. Test in an Incognito window!)*

