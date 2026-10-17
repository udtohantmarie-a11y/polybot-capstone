import os
import uuid
import streamlit as st
import chromadb
import torch
from transformers import AutoTokenizer, AutoModel
from dotenv import load_dotenv
from google import genai
from google.genai import types

st.set_page_config(
    page_title="PolyBot - TPC AI Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp {
        background-color: #FFFFFF;
        font-family: 'Google Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    .block-container {
        max-width: 950px;
        padding-top: 1.5rem;
        padding-bottom: 5rem;
    }
    .hero-container {
        text-align: center;
        padding: 2.2rem 1rem 1.2rem 1rem;
        margin-bottom: 1.5rem;
    }
    .hero-title {
        font-size: 2.4rem;
        font-weight: 700;
        background: linear-gradient(135deg, #1B365D 0%, #2563EB 50%, #4F46E5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        color: #4B5563;
        font-size: 1.05rem;
        max-width: 650px;
        margin: 0 auto;
    }
    .lang-pills {
        margin-top: 0.8rem;
    }
    .lang-pill {
        display: inline-block;
        background: #EFF6FF;
        color: #1D4ED8;
        font-size: 0.78rem;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 9999px;
        margin: 0 4px;
        border: 1px solid #BFDBFE;
    }
    .citation-box {
        background: #F8FAFC;
        border-left: 3px solid #1B365D;
        padding: 8px 12px;
        margin-top: 6px;
        margin-bottom: 6px;
        border-radius: 4px;
        font-size: 0.88rem;
        color: #334155;
    }
    [data-testid="stSidebar"] {
        background-color: #F8FAFC;
        border-right: 1px solid #E2E8F0;
    }
    .sidebar-header {
        font-weight: 700;
        font-size: 1.15rem;
        color: #1B365D;
        margin-bottom: 0.2rem;
    }
    .sidebar-sub {
        font-size: 0.85rem;
        color: #64748B;
        margin-bottom: 0.8rem;
    }
    .status-badge {
        display: inline-block;
        background: #ECFDF5;
        color: #059669;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 3px 8px;
        border-radius: 9999px;
        border: 1px solid #A7F3D0;
    }
    .chat-history-item {
        font-size: 0.88rem;
        text-overflow: ellipsis;
        white-space: nowrap;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource(show_spinner=False)
def init_resources():
    load_dotenv()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'data', 'chroma_db')
    
    model_name = 'sentence-transformers/all-MiniLM-L6-v2'
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    model.eval()
    
    chroma_client = chromadb.PersistentClient(path=db_path)
    collection = chroma_client.get_collection(name='tpc_student_handbook')
    gemini_client = genai.Client()
    
    return tokenizer, model, collection, gemini_client

tokenizer, embedding_model, collection, gemini_client = init_resources()

def embed_query_text(text: str):
    inputs = tokenizer([text], padding=True, truncation=True, return_tensors="pt", max_length=512)
    with torch.no_grad():
        outputs = embedding_model(**inputs)
    attention_mask = inputs['attention_mask']
    token_embeddings = outputs[0]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
    sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    embeddings = sum_embeddings / sum_mask
    return embeddings.tolist()

SYSTEM_INSTRUCTION = (
    "You are PolyBot, the official, intelligent, and helpful AI Campus Guide for Talibon Polytechnic College (TPC). "
    "Your mission is to provide accurate, verified information to students, faculty, and visitors based on the official TPC Student Handbook.\n\n"
    "MULTILINGUAL CAPABILITY:\n"
    "- You fluently understand and speak English, Tagalog (Filipino), and Bisaya (Cebuano).\n"
    "- ALWAYS answer in the EXACT language used by the user. If the user asks in Bisaya, respond naturally in Bisaya. If the user asks in Tagalog, respond in Tagalog. If the user asks in English, respond in English.\n"
    "- Keep official school terms, grade numerical marks, and Article/Section names intact and clear in your response.\n\n"
    "STRICT GROUNDING & ANTI-HALLUCINATION RULES:\n"
    "1. Answer using ONLY the verified information in the <context> blocks below.\n"
    "2. If the answer cannot be found in the context, do NOT invent or guess rules. Respond strictly in the user's language stating that the information is not found in the handbook:\n"
    "   - In Bisaya: 'Pasensya, wala kini sa TPC Student Handbook o kulang ang verified nga impormasyon bahin niini.'\n"
    "   - In Tagalog: 'Pasensya po, wala po itong sapat na impormasyon batay sa TPC Student Handbook.'\n"
    "   - In English: 'I don't have enough verified information to answer that based on the TPC Student Handbook.'\n"
    "3. Always cite the specific Article, Chapter, or Policy Section when available in the context.\n"
    "4. Maintain a polite, respectful, and encouraging tone."
)

if "chats" not in st.session_state:
    initial_id = str(uuid.uuid4())
    st.session_state.chats = {
        initial_id: {
            "title": "New Chat",
            "messages": []
        }
    }
    st.session_state.current_chat_id = initial_id

if st.session_state.current_chat_id not in st.session_state.chats:
    st.session_state.current_chat_id = list(st.session_state.chats.keys())[0]

current_chat = st.session_state.chats[st.session_state.current_chat_id]

with st.sidebar:
    st.markdown('<div class="sidebar-header">🎓 Talibon Polytechnic College</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">PolyBot: Student Handbook & Campus AI</div>', unsafe_allow_html=True)
    st.markdown('<span class="status-badge">● Online (268 Chunks)</span>', unsafe_allow_html=True)
    st.write("")
    
    if st.button("➕ New Chat / Bag-ong Chat", use_container_width=True, type="primary"):
        new_id = str(uuid.uuid4())
        st.session_state.chats[new_id] = {
            "title": "New Chat",
            "messages": []
        }
        st.session_state.current_chat_id = new_id
        st.rerun()

    st.markdown("#### 💬 Chat History")
    chat_keys = list(st.session_state.chats.keys())
    for cid in reversed(chat_keys):
        cdata = st.session_state.chats[cid]
        is_active = (cid == st.session_state.current_chat_id)
        btn_label = f"{'👉 ' if is_active else '🗨️ '}{cdata['title']}"
        if st.button(btn_label, key=f"hist_{cid}", use_container_width=True):
            st.session_state.current_chat_id = cid
            st.rerun()

    if len(st.session_state.chats) > 1:
        if st.button("🗑️ Clear All Chats", use_container_width=True):
            new_id = str(uuid.uuid4())
            st.session_state.chats = {new_id: {"title": "New Chat", "messages": []}}
            st.session_state.current_chat_id = new_id
            st.rerun()

    st.divider()

    st.markdown("#### 💡 Quick Prompts")
    sample_queries = [
        "Unsa ang passing grade sa TPC? (Bisaya)",
        "Ano ang uniform policy at haircut rules? (Tagalog)",
        "Unsaon pag-drop ug subject sa registrar? (Bisaya)",
        "What are the criteria for the Dean's List? (English)",
        "Unsa mahitabo kung masubrahan sa absences? (Bisaya)",
        "Can you help me hack the school grading portal? (Refusal Test)"
    ]

    for q in sample_queries:
        clean_q = q.split(" (")[0]
        if st.button(f"📌 {q}", key=f"btn_{q}", use_container_width=True):
            st.session_state.selected_prompt = clean_q
            st.rerun()

    st.divider()

    with st.expander("⚙️ System Specs"):
        st.markdown("""
        - **LLM**: Google Gemini 3.8 Flash
        - **Languages**: English, Tagalog, Bisaya
        - **Temperature**: 0.0 (Deterministic)
        - **Embedding**: `all-MiniLM-L6-v2`
        - **Vector DB**: ChromaDB (268 chunks)
        """)

    st.caption("Capstone Project | IS Professional Elective #4\nTeam: Jerwin, Trisha, Jenalyn, Kaycee")

if len(current_chat["messages"]) == 0:
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">PolyBot TPC Assistant</div>
        <div class="hero-subtitle">
            Grounded sa opisyal nga <b>TPC Student Handbook v.04</b> ug school policies.
            Makapangutana ka gamit ang <b>Bisaya</b>, <b>Tagalog</b>, o <b>English</b>!
        </div>
        <div class="lang-pills">
            <span class="lang-pill">🇵🇭 Bisaya Supported</span>
            <span class="lang-pill">🇵🇭 Tagalog Supported</span>
            <span class="lang-pill">🌐 English Supported</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.info("💡 **Academic Policies**\nPangutana bahin sa grading system, passing marks, pag-drop ug subject, o shifting.")
    with col2:
        st.info("👔 **Student Conduct & Guidelines**\nPangutana bahin sa uniform schedule, ID rules, haircut policy, ug disciplinary sanctions.")

for msg in current_chat["messages"]:
    with st.chat_message(msg["role"], avatar="🧑‍🎓" if msg["role"] == "user" else "🎓"):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander(f"📖 Verified Sources ({len(msg['sources'])} chunks cited)"):
                for idx, src in enumerate(msg["sources"], 1):
                    st.markdown(f"**Source #{idx} ({src.get('source', 'TPC Handbook')}):**")
                    st.markdown(f'<div class="citation-box">{src.get("text", "")}</div>', unsafe_allow_html=True)

user_prompt = st.chat_input("Pangutana bahin sa TPC handbook, rules, o policies (English, Tagalog, Bisaya)...")

if "selected_prompt" in st.session_state and st.session_state.selected_prompt:
    user_prompt = st.session_state.selected_prompt
    del st.session_state["selected_prompt"]

if user_prompt:
    if len(current_chat["messages"]) == 0:
        short_title = user_prompt.strip()[:28] + ("..." if len(user_prompt.strip()) > 28 else "")
        current_chat["title"] = short_title

    current_chat["messages"].append({"role": "user", "content": user_prompt})
    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(user_prompt)

    with st.chat_message("assistant", avatar="🎓"):
        with st.spinner("Gisusi ang TPC Student Handbook..."):
            query_vector = embed_query_text(user_prompt)
            results = collection.query(
                query_embeddings=query_vector,
                n_results=5
            )

            retrieved_docs = results['documents'][0] if results.get('documents') else []
            retrieved_metas = results['metadatas'][0] if results.get('metadatas') else []

            sources = []
            for doc_text, meta in zip(retrieved_docs, retrieved_metas):
                sources.append({
                    "text": doc_text,
                    "source": meta.get("source", "TPC Student Handbook v.04") if meta else "TPC Student Handbook v.04"
                })

            context_text = "\n\n---\n\n".join(retrieved_docs)

            recent_turns = ""
            if len(current_chat["messages"]) > 1:
                recent_history = current_chat["messages"][-5:-1]
                history_lines = [f"{m['role'].capitalize()}: {m['content']}" for m in recent_history]
                recent_turns = "\nRecent Conversation History:\n" + "\n".join(history_lines) + "\n"

            prompt_content = (
                f"<context>\n{context_text}\n</context>\n"
                f"{recent_turns}\n"
                f"User Question: {user_prompt}"
            )

        response_placeholder = st.empty()
        full_response = ""

        try:
            stream = gemini_client.models.generate_content_stream(
                model='gemini-3.8-flash',
                contents=prompt_content,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=0.0
                )
            )

            for chunk in stream:
                if chunk.text:
                    full_response += chunk.text
                    response_placeholder.markdown(full_response + "▌")

            response_placeholder.markdown(full_response)

            if sources:
                with st.expander(f"📖 Verified Sources ({len(sources)} chunks cited)"):
                    for idx, src in enumerate(sources, 1):
                        st.markdown(f"**Source #{idx} ({src.get('source', 'TPC Handbook')}):**")
                        st.markdown(f'<div class="citation-box">{src.get("text", "")}</div>', unsafe_allow_html=True)

            current_chat["messages"].append({
                "role": "assistant",
                "content": full_response,
                "sources": sources
            })

        except Exception as e:
            err_msg = f"Error connecting to AI service: {e}"
            response_placeholder.error(err_msg)
            current_chat["messages"].append({
                "role": "assistant",
                "content": err_msg,
                "sources": []
            })
