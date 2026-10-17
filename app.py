import os
import streamlit as st
import chromadb
import torch
from transformers import AutoTokenizer, AutoModel
from dotenv import load_dotenv
from google import genai
from google.genai import types

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="PolyBot - TPC AI Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# CUSTOM GEMINI-STYLE CSS
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Google / Gemini aesthetic clean styling */
    .stApp {
        background-color: #FFFFFF;
        font-family: 'Google Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Main container max width */
    .block-container {
        max-width: 950px;
        padding-top: 1.5rem;
        padding-bottom: 5rem;
    }

    /* Hero welcome header */
    .hero-container {
        text-align: center;
        padding: 2.5rem 1rem 1.5rem 1rem;
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
        max-width: 600px;
        margin: 0 auto;
    }

    /* Suggestion cards */
    .suggestion-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 12px 16px;
        cursor: pointer;
        transition: all 0.2s ease;
        text-align: left;
    }
    .suggestion-card:hover {
        background: #EFF6FF;
        border-color: #3B82F6;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.08);
    }

    /* Citations expander */
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

    /* Sidebar custom styling */
    [data-testid="stSidebar"] {
        background-color: #F8FAFC;
        border-right: 1px solid #E2E8F0;
    }
    .sidebar-header {
        font-weight: 700;
        font-size: 1.15rem;
        color: #1B365D;
        margin-bottom: 0.25rem;
    }
    .sidebar-sub {
        font-size: 0.85rem;
        color: #64748B;
        margin-bottom: 1rem;
    }

    /* Badge */
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
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# CACHED RESOURCE INITIALIZATION
# -----------------------------------------------------------------------------
@st.cache_resource(show_spinner="Initializing PolyBot AI engine & vector store...")
def init_resources():
    load_dotenv()
    
    # Paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'data', 'chroma_db')
    
    # 1. HuggingFace Embedding Model (sentence-transformers/all-MiniLM-L6-v2)
    model_name = 'sentence-transformers/all-MiniLM-L6-v2'
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    model.eval()
    
    # 2. ChromaDB Persistent Client & Collection
    chroma_client = chromadb.PersistentClient(path=db_path)
    collection = chroma_client.get_collection(name='tpc_student_handbook')
    
    # 3. Google Gemini Client
    gemini_client = genai.Client()
    
    return tokenizer, model, collection, gemini_client

tokenizer, embedding_model, collection, gemini_client = init_resources()

# -----------------------------------------------------------------------------
# RAG HELPER FUNCTIONS
# -----------------------------------------------------------------------------
def embed_query_text(text: str):
    """Generates 384-dimensional dense embedding for query."""
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
    "You are PolyBot, the official and intelligent AI Campus Guide for Talibon Polytechnic College (TPC). "
    "Your mission is to provide accurate, verified information to students, faculty, and visitors. "
    "Strict Grounding Rules:\n"
    "1. Answer using ONLY the verified information provided in the <context> blocks below.\n"
    "2. If the user question cannot be answered from the provided context, respond EXACTLY with:\n"
    "   'I don't have enough verified information to answer that based on the TPC Student Handbook.'\n"
    "3. Never guess, assume, or fabricate school policies or rules.\n"
    "4. Always cite the specific Article, Chapter, or Policy Section when available in the context.\n"
    "5. Be polite, formal, encouraging, and clear."
)

# -----------------------------------------------------------------------------
# SESSION STATE (CONVERSATIONAL MEMORY - DELIVERABLE 12)
# -----------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="sidebar-header">🎓 Talibon Polytechnic College</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">PolyBot: Student Handbook & Campus AI</div>', unsafe_allow_html=True)
    
    st.markdown('<span class="status-badge">● RAG Online (268 Chunks)</span>', unsafe_allow_html=True)
    st.write("")
    
    if st.button("➕ New Conversation", use_container_width=True, type="primary"):
        st.session_state.messages = []
        st.rerun()
        
    st.divider()
    
    st.markdown("#### 💡 Quick Questions")
    sample_queries = [
        "What is the grading system and passing grade?",
        "What are the rules regarding student uniform?",
        "How can a student officially drop a subject?",
        "What are the criteria for the Dean's List?",
        "What happens if I exceed the limit on absences?",
        "Can you help me hack the school grading portal?"
    ]
    
    for q in sample_queries:
        if st.button(f"📌 {q}", key=f"btn_{q}", use_container_width=True):
            st.session_state.selected_prompt = q
            st.rerun()

    st.divider()
    
    with st.expander("⚙️ System Architecture & Specs"):
        st.markdown("""
        - **LLM**: Google Gemini 3.8 Flash
        - **Temperature**: 0.0 (Deterministic)
        - **Embedding**: `all-MiniLM-L6-v2` (384-dim)
        - **Vector Store**: ChromaDB (Cosine Similarity)
        - **Memory**: Multi-Turn Session State
        """)
        
    st.caption("Capstone Project | IS Professional Elective #4\nTeam: Jerwin, Trisha, Jenalyn, Kaycee")

# -----------------------------------------------------------------------------
# MAIN CHAT DISPLAY
# -----------------------------------------------------------------------------
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">PolyBot TPC Assistant</div>
        <div class="hero-subtitle">
            Welcome! I am your AI guide grounded directly in the <b>TPC Student Handbook v.04</b> and official campus documents. 
            Ask me anything about grading, academic policies, campus rules, and guidelines.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick launch cards
    col1, col2 = st.columns(2)
    with col1:
        st.info("💡 **Academic Policies**\nAsk about grading rubrics, passing marks, shifting, and graduation requirements.")
    with col2:
        st.info("👔 **Student Life & Conduct**\nInquire about campus dress code, uniform schedules, and student disciplinary codes.")

# Display existing chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🧑‍🎓" if msg["role"] == "user" else "🎓"):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander(f"📖 View Verified Sources ({len(msg['sources'])} chunks cited)"):
                for idx, src in enumerate(msg["sources"], 1):
                    st.markdown(f"**Source #{idx} ({src.get('source', 'TPC Handbook')}):**")
                    st.markdown(f'<div class="citation-box">{src.get("text", "")}</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# HANDLE USER INPUT
# -----------------------------------------------------------------------------
user_prompt = st.chat_input("Ask PolyBot about TPC student handbook, rules, or policies...")

# Check if a sidebar prompt button was clicked
if "selected_prompt" in st.session_state and st.session_state.selected_prompt:
    user_prompt = st.session_state.selected_prompt
    del st.session_state["selected_prompt"]

if user_prompt:
    # 1. Append user message to state
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(user_prompt)

    # 2. Vector Retrieval (ChromaDB)
    with st.chat_message("assistant", avatar="🎓"):
        with st.spinner("Searching official TPC Student Handbook..."):
            query_vector = embed_query_text(user_prompt)
            results = collection.query(
                query_embeddings=query_vector,
                n_results=5
            )
            
            retrieved_docs = results['documents'][0] if results.get('documents') else []
            retrieved_metas = results['metadatas'][0] if results.get('metadatas') else []
            
            # Formulate sources list
            sources = []
            for doc_text, meta in zip(retrieved_docs, retrieved_metas):
                sources.append({
                    "text": doc_text,
                    "source": meta.get("source", "TPC Student Handbook v.04") if meta else "TPC Student Handbook v.04"
                })
            
            context_text = "\n\n---\n\n".join(retrieved_docs)
            
            # Multi-turn memory assembly (last 2 turns)
            recent_turns = ""
            if len(st.session_state.messages) > 1:
                recent_history = st.session_state.messages[-3:-1]
                history_lines = [f"{m['role'].capitalize()}: {m['content']}" for m in recent_history]
                recent_turns = "\nPrevious Conversation:\n" + "\n".join(history_lines) + "\n"

            prompt_content = (
                f"<context>\n{context_text}\n</context>\n"
                f"{recent_turns}\n"
                f"Current User Question: {user_prompt}"
            )

        # 3. Stream Gemini Response
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
            
            # Show citations expander
            if sources:
                with st.expander(f"📖 View Verified Sources ({len(sources)} chunks cited)"):
                    for idx, src in enumerate(sources, 1):
                        st.markdown(f"**Source #{idx} ({src.get('source', 'TPC Handbook')}):**")
                        st.markdown(f'<div class="citation-box">{src.get("text", "")}</div>', unsafe_allow_html=True)

            # Store to history
            st.session_state.messages.append({
                "role": "assistant",
                "content": full_response,
                "sources": sources
            })

        except Exception as e:
            err_msg = f"Sorry, an error occurred while connecting to Gemini: {e}"
            response_placeholder.error(err_msg)
            st.session_state.messages.append({
                "role": "assistant",
                "content": err_msg,
                "sources": []
            })

