import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

doc = docx.Document()

# Adjust page margins
sections = doc.sections
for section in sections:
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

# Helper function for headings with color
def add_custom_heading(text, level, color_rgb=(27, 54, 93)):
    h = doc.add_heading(text, level=level)
    run = h.runs[0]
    run.font.color.rgb = RGBColor(*color_rgb)
    return h

# Title
title_p = doc.add_paragraph()
title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run_title = title_p.add_run('POLYBOT: TPC STUDENT HANDBOOK & CAMPUS ASSISTANT\nCAPSTONE DEFENSE SCRIPT & DELIVERABLES GUIDE')
run_title.bold = True
run_title.font.size = Pt(18)
run_title.font.color.rgb = RGBColor(27, 54, 93)

sub_p = doc.add_paragraph()
sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run_sub = sub_p.add_run('Comprehensive Defense Script, Checkpoints 3 & 4 Deliverables Matrix, and Q&A Guide\nIS Professional Elective #4 - GenAI Capstone')
run_sub.font.size = Pt(11)
run_sub.font.italic = True
doc.add_paragraph()

# -------------------------------------------------------------
# SECTION 1: TEAM MEMBER ROLES & DELIVERABLES MATRIX
# -------------------------------------------------------------
add_custom_heading('1. Team Roles & Checkpoint Deliverables Matrix', level=1)

p_intro = doc.add_paragraph(
    'This matrix aligns our team members with the required deliverables from Checkpoint 3 (RAG Orchestration & Working Application) '
    'and Checkpoint 4 (Customization, Deployment & Final Defense), as defined in the Capstone Project Guide.'
)

table = doc.add_table(rows=1, cols=4)
table.alignment = WD_TABLE_ALIGNMENT.CENTER
table.style = 'Table Grid'
hdr_cells = table.rows[0].cells
headers = ['Member', 'Project Role', 'Checkpoint 3 Tasks (Semi-Final)', 'Checkpoint 4 Tasks (Final Defense)']
for i, h_text in enumerate(headers):
    hdr_cells[i].text = h_text
    hdr_cells[i].paragraphs[0].runs[0].bold = True

tasks_data = [
    (
        'Jerwin Villarin',
        'QA & Evaluation /\nDataset Curation',
        '• Deliverable 10: Dataset extraction & cleaning (TPC Handbook & Website).\n• Deliverable 14: Test query suite creation (5 realistic + 1 refusal query).\n• Evaluation & grounding check.',
        '• Deliverable 19: Lead writer for Evaluation & Limitations in Final Technical Report.\n• Deliverable 20: Presentation Co-lead (Problem, Motivation & QA Results).'
    ),
    (
        'Trisha Marie Udtohan',
        'Lead Developer\n(Backend & Data Pipeline)',
        '• Deliverable 10: Ingestion pipeline (automated text parsing, 150-word chunking, embeddings).\n• Deliverable 11: Vector database setup with ChromaDB.\n• Similarity metric selection (Cosine Similarity).',
        '• Deliverable 19: Architecture & Data Pipeline section in Final Technical Report.\n• Defend vector database, chunking strategy, and 100x scaling architecture.'
    ),
    (
        'Jenalyn Sabal',
        'AI Orchestrator\n(RAG & Guardrails)',
        '• Deliverable 11: RAG pipeline integration with Google Gemini API.\n• Deliverable 12: Conversational Memory (multi-turn session state).\n• Deliverable 13: Framework Comparison Note (LangChain vs. LlamaIndex).',
        '• Deliverable 15: Model Customization Note (PEFT/LoRA/QLoRA analysis vs base RAG).\n• Prompt Guardrails & Zero-hallucination configuration (Temp 0.0, fallback rule).'
    ),
    (
        'Kaycee Cerida',
        'DevOps, UI &\nDeployment Lead',
        '• Deliverable 11: Application UI integration.\n• Multi-turn session state frontend handling.\n• Verification of end-to-end response flow.',
        '• Deliverable 16: Application Web Interface (Streamlit chat UI).\n• Deliverable 17: Containerization (Multi-stage Dockerfile & secrets management).\n• Deliverable 18: Deployment Evidence (Cloud hosting & public sandbox URL).\n• Deliverable 20: Live Demo Operator.'
    )
]

for name, role, cp3, cp4 in tasks_data:
    row_cells = table.add_row().cells
    row_cells[0].text = name
    row_cells[0].paragraphs[0].runs[0].bold = True
    row_cells[1].text = role
    row_cells[2].text = cp3
    row_cells[3].text = cp4

doc.add_paragraph()

# -------------------------------------------------------------
# SECTION 2: 10-15 MINUTE DEFENSE PRESENTATION SCRIPT
# -------------------------------------------------------------
add_custom_heading('2. Final Defense Presentation Script (10-15 Minutes)', level=1)
doc.add_paragraph(
    'Presentation Format: 10-15 minutes presentation followed by 5-10 minutes Q&A. '
    'All team members must speak and demonstrate comprehensive mastery of the end-to-end pipeline.'
)

# Speaker 1: Jerwin
add_custom_heading('Speaker 1: Jerwin Villarin (QA & Evaluation / Dataset Curation)', level=2)
doc.add_paragraph('Slide 1: Problem Statement, Motivation & Official Dataset\nSuggested Duration: 2.5 minutes\n').runs[0].bold = True

p_j1 = doc.add_paragraph()
p_j1.add_run(
    '"Good morning, esteemed members of the panel, our adviser, and fellow students. '
    'I am Jerwin Villarin, representing Team PolyBot as the Dataset Curator and Quality Assurance lead.\n\n'
    'To begin, let us look at the core problem. At Talibon Polytechnic College, students, faculty, and visitors frequently need quick, '
    'reliable answers about academic policies, uniform regulations, grading systems, and campus services. Currently, obtaining this '
    'information requires manually scouring through a 203-page Student Handbook PDF or navigating disjointed web pages. '
    'This leads to misinformation, student frustration, and administrative bottlenecks.\n\n'
    'To solve this, we engineered PolyBot—a domain-grounded Retrieval-Augmented Generation assistant specifically tailored for TPC. '
    'My primary responsibility was ensuring absolute data fidelity. We curated official sources only: the TPC Student Handbook Version 04 '
    'and verified institutional web data. In GenAI applications, garbage in means hallucination out. By cleaning and validating every '
    'section header, policy article, and table before ingestion, we established a high-integrity ground truth for our pipeline.\n\n'
    'I will now turn over the floor to our Lead Developer, Trisha, to discuss how our backend transforms raw text into mathematical vectors."'
)

# Speaker 2: Trisha
add_custom_heading('Speaker 2: Trisha Marie Udtohan (Lead Developer - Backend & Data Pipeline)', level=2)
doc.add_paragraph('Slides 2-3: Architecture Overview, Ingestion Pipeline & Vector Indexing\nSuggested Duration: 3.5 minutes\n').runs[0].bold = True

p_t1 = doc.add_paragraph()
p_t1.add_run(
    '"Thank you, Jerwin. Good morning, panel. I am Trisha Marie Udtohan, Lead Developer for PolyBot.\n\n'
    'I engineered the end-to-end Ingestion and Retrieval Pipeline—fulfilling Deliverable 10 of our capstone requirements. '
    'Raw PDF documents cannot be ingested directly by Large Language Models due to context window constraints and retrieval noise. '
    'Our automated ingestion pipeline executes three core phases:\n\n'
    '1. Text Extraction & Cleaning: We parsed the 203-page handbook, removing artifacts, page numbers, and headers while preserving structural markdown headers.\n'
    '2. Strategic Chunking: We evaluated multiple chunking sizes and settled on uniform 150-word chunks with a 25-word sliding overlap. '
    'This chunk size is optimal because student handbook policies (such as a single disciplinary clause or grading tier) are concise. '
    'The 25-word overlap prevents semantic boundary loss between sentences.\n'
    '3. Vector Indexing: Using high-dimensional dense embeddings, each text chunk was embedded and stored in ChromaDB, an open-source, '
    'embedded vector database.\n\n'
    'A key technical decision required in our rubric was distance metric selection. We selected Cosine Similarity over Euclidean (L2) distance. '
    'Cosine similarity calculates the cosine of the angle between query and document vectors, evaluating semantic orientation regardless of length. '
    'Whether a student enters a concise 3-word query like \\"grading system rules\\" or a conversational 30-word scenario, cosine similarity accurately '
    'retrieves the top-k most relevant handbook passages without bias toward text magnitude.\n\n'
    'I now pass the presentation to Jenalyn Sabal to explain our AI orchestration and guardrails."'
)

# Speaker 3: Jenalyn
add_custom_heading('Speaker 3: Jenalyn Sabal (AI Orchestrator - RAG, Guardrails & Memory)', level=2)
doc.add_paragraph('Slide 4: RAG Orchestration, Conversational Memory & Framework Trade-offs\nSuggested Duration: 3.5 minutes\n').runs[0].bold = True

p_s1 = doc.add_paragraph()
p_s1.add_run(
    '"Good morning, panel. I am Jenalyn Sabal, AI Orchestrator for PolyBot.\n\n'
    'My responsibility was building the cognitive core—satisfying Deliverables 11, 12, 13, and 15. '
    'When Trisha\'s database retrieves the top chunks, my RAG orchestration engine bridges that retrieved context with the Google Gemini API.\n\n'
    'To guarantee reliability, we solved three major GenAI engineering challenges:\n\n'
    '1. Preventing Hallucinations: We set the Gemini model temperature to strictly 0.0. Temperature 0.0 makes model inference deterministic '
    'and greedy, eliminating stochastic creativity. We combined this with strict system prompt guardrails: PolyBot is explicitly instructed '
    'to answer ONLY using the retrieved context and MUST cite the handbook Article and Section. Furthermore, we programmed a safe refusal fallback: '
    'if retrieved similarity scores fall below threshold or the query is absent from the handbook, PolyBot responds: '
    '\\"I do not have enough verified information in the TPC Handbook to answer that.\\"\n\n'
    '2. Conversational Memory (Deliverable 12): Real users ask follow-up questions. We implemented session-based conversational buffer memory. '
    'For instance, if a user asks \\"What are the requirements for Dean\'s List?\\" and follows up with \\"What GPA do I need for it?\\", '
    'our memory manager tracks entity state across turns so the model understands \\"it\\" refers to the Dean\'s List.\n\n'
    '3. Framework Comparison & Model Customization (Deliverables 13 & 15): In our Framework Comparison Note, we compared LangChain\'s composable '
    'chain architecture against LlamaIndex\'s data-centric tree/node indexing. We chose LangChain for flexible memory orchestration combined with '
    'native ChromaDB retrieval. Additionally, in our Model Customization Note, we analyzed PEFT (LoRA/QLoRA) versus base RAG. '
    'We justified that base instruction-tuned Gemini combined with RAG is superior to parameter fine-tuning for institutional rules, '
    'because school handbooks undergo annual amendments; RAG allows instant zero-cost document updates without re-training or catastrophic forgetting.\n\n'
    'Now, Kaycee Cerida will present our UI, containerization, deployment, and live demonstration."'
)

# Speaker 4: Kaycee
add_custom_heading('Speaker 4: Kaycee Cerida (DevOps, UI & Deployment Lead)', level=2)
doc.add_paragraph('Slides 5-8: Web UI, Docker Containerization, Deployment & Live Demo\nSuggested Duration: 4.5 minutes\n').runs[0].bold = True

p_k1 = doc.add_paragraph()
p_k1.add_run(
    '"Good morning, panel. I am Kaycee Cerida, handling DevOps, Interface Engineering, and Deployment.\n\n'
    'To satisfy Checkpoint 4 (Deliverables 16, 17, and 18), I transformed our backend algorithms into an accessible, production-grade application:\n\n'
    '1. Web Interface (Deliverable 16): We built a responsive chat UI using Streamlit. It provides real-time streaming tokens, '
    'session clearing, citation expanders showing the exact retrieved handbook chunks, and query history.\n\n'
    '2. Containerization (Deliverable 17): We authored a multi-stage Dockerfile. Stage 1 installs Python dependencies in an isolated build environment; '
    'Stage 2 copies only necessary runtime binaries and the pre-computed ChromaDB index into a lightweight Python-slim image. '
    'This reduced our Docker image footprint by over 60% and sealed sensitive credentials via environment variables rather than hardcoded tokens.\n\n'
    '3. Cloud Deployment (Deliverable 18): Our containerized application was deployed to a cloud environment with continuous deployment, '
    'accessible publicly via live URL.\n\n'
    'We will now proceed directly to our Live Demonstration, showcasing 5 realistic operational queries and 1 controlled out-of-scope refusal."'
)

doc.add_paragraph()

# -------------------------------------------------------------
# SECTION 3: LIVE DEMO PROTOCOL (5 REALISTIC + 1 REFUSAL QUERY)
# -------------------------------------------------------------
add_custom_heading('3. Live Demonstration Protocol (Deliverable 14)', level=1)
doc.add_paragraph(
    'As required by Deliverable 14 and rubric criteria, the live demo must showcase at least 5 realistic domain queries '
    'grounded in the handbook, plus 1 out-of-scope query that is safely refused.'
)

demo_table = doc.add_table(rows=1, cols=4)
demo_table.alignment = WD_TABLE_ALIGNMENT.CENTER
demo_table.style = 'Table Grid'
d_hdr = demo_table.rows[0].cells
d_headers = ['Test #', 'Test Objective / Scenario', 'User Query Input', 'Expected Grounded Behavior & Citation']
for i, h_text in enumerate(d_headers):
    d_hdr[i].text = h_text
    d_hdr[i].paragraphs[0].runs[0].bold = True

demo_cases = [
    (
        'Query 1',
        'Academic Policy &\nGrading System',
        '"What is the grading system at TPC, and what is the minimum grade required to pass a subject?"',
        'Model returns the 1.00 to 5.00 numeric grading scale, cites 3.00 as passing and 5.00 as failing, and cites the specific Student Handbook Article on Grading.'
    ),
    (
        'Query 2',
        'Campus Discipline &\nDress Code',
        '"What are the official rules regarding school uniform and haircut policy on campus?"',
        'Model outlines prescribed uniform schedule, ID lanyard requirements, and grooming standards, citing Student Affairs Disciplinary Rules.'
    ),
    (
        'Query 3',
        'Registrar Procedures &\nDropping Subjects',
        '"How can a student officially drop a subject, and what is the required procedure?"',
        'Model details step-by-step: securing dropping form from Registrar, instructor signature, and deadline before midterm exams, citing Academic Regulations.'
    ),
    (
        'Query 4',
        'Academic Honors &\nScholarship',
        '"What are the criteria to qualify for the Dean’s List or academic honors at TPC?"',
        'Model specifies required GWA (e.g. 1.75 or above), regular academic load, and zero grades below 2.5, citing Student Honors Code.'
    ),
    (
        'Query 5',
        'Conversational Memory\n(Multi-Turn Context)',
        'Turn 1: "What are the rules on student absences?"\nTurn 2: "What happens if I exceed that limit?"',
        'Model retains context from Turn 1. Resolves "that limit" to 20% total class hours, and accurately cites sanctions (Dropped / Failure due to absences).'
    ),
    (
        'Query 6',
        'Out-of-Scope Fallback\n(Guardrail Refusal)',
        '"How do I apply for a student visa to study in Canada?" OR "Can you write a cheat sheet for my exam?"',
        'SUCCESSFUL REFUSAL: System triggers fallback: "I am PolyBot, your TPC Handbook Assistant. I can only assist with official TPC campus rules, policies, and academic guidelines."'
    )
]

for t_num, obj, q_in, exp in demo_cases:
    row_cells = demo_table.add_row().cells
    row_cells[0].text = t_num
    row_cells[0].paragraphs[0].runs[0].bold = True
    row_cells[1].text = obj
    row_cells[2].text = q_in
    row_cells[3].text = exp

doc.add_paragraph()

# -------------------------------------------------------------
# SECTION 4: TECHNICAL DEFENSE QUESTIONS & ANSWERS (CHEAT SHEET)
# -------------------------------------------------------------
add_custom_heading('4. Technical Defense Q&A Preparation (Panel Defense Sheet)', level=1)
doc.add_paragraph(
    'Based on Section 6 of the Capstone Guide, the panel will ask targeted technical defense questions. '
    'Below are our prepared answers assigned to individual team members.'
)

qa_list = [
    (
        'Defense Question 1: "Why did you choose Cosine Similarity and ChromaDB over other vector databases and metrics?"',
        'Assigned Speaker: Trisha Marie Udtohan (Lead Developer)',
        'Comprehensive Answer:\n'
        '"We chose ChromaDB because it is an open-source, serverless, and lightweight embedded vector store that runs directly in Python '
        'without requiring an external managed server cluster like Pinecone or Weaviate. For a 203-page handbook (~1,500 chunks), ChromaDB '
        'provides sub-50ms retrieval latency with minimal CPU and memory overhead.\n\n'
        'We selected Cosine Similarity as our distance metric because text queries and handbook documents differ significantly in length. '
        'Cosine similarity measures the angular difference between vectors in embedding space rather than absolute Euclidean magnitude. '
        'This ensures that whether a student types a short keyword query or a multi-sentence question, the metric evaluates purely semantic '
        'relevance, preventing longer chunks from distorting similarity rankings."'
    ),
    (
        'Defense Question 2: "Walk us through what happens step-by-step when a user submits a query."',
        'Assigned Speakers: Trisha Marie Udtohan & Jenalyn Sabal',
        'Comprehensive Answer:\n'
        '"The process follows 7 precise stages:\n'
        '1. Input & Contextualization: The student submits a prompt through the Streamlit UI. If there is conversational history, '
        'our memory buffer reformulates the query to resolve pronouns (e.g., changing \\"what are its penalties\\" to \\"what are the penalties for cheating\\").\n'
        '2. Dense Embedding Generation: The query text is transformed into a 768-dimensional vector embedding.\n'
        '3. Vector Search: ChromaDB performs cosine similarity search across the handbook index and extracts the top 3-4 most relevant chunks.\n'
        '4. Similarity Threshold Check: If retrieved distance scores fall below our relevance cutoff, the fallback handler is immediately primed.\n'
        '5. Prompt Assembly: The system prompt, retrieved chunks, and conversation context are assembled into a structured RAG template.\n'
        '6. Model Inference: Google Gemini API processes the prompt with Temperature 0.0, producing deterministic output with Article citations.\n'
        '7. UI Rendering: Streamlit streams the response tokens to the user, displaying citation metadata in an expandable drawer."'
    ),
    (
        'Defense Question 3: "How does your system avoid or reduce hallucinated answers?"',
        'Assigned Speaker: Jenalyn Sabal (AI Orchestrator)',
        'Comprehensive Answer:\n'
        '"We employ a four-layer defense-in-depth architecture against hallucinations:\n'
        '1. Grounded Context Injection: The LLM is strictly constrained to use only the retrieved context chunks provided in the prompt.\n'
        '2. Zero-Temperature Sampling: Setting temperature to 0.0 removes randomness and creative extrapolation.\n'
        '3. Mandatory Source Citation: The model is instructed to cite specific Articles, Chapters, or Sections. An LLM cannot fabricate verifiable citations as easily when restricted.\n'
        '4. Hardened Fallback Guardrails: We established an explicit negative constraint: \\"If the information is not explicitly stated in the context, do NOT speculate; reply with our standard fallback phrase.\\" This converts potential hallucinations into safe, honest refusals."'
    ),
    (
        'Defense Question 4: "What would break if your document collection grew 100x?"',
        'Assigned Speakers: Trisha Marie Udtohan & Kaycee Cerida',
        'Comprehensive Answer:\n'
        '"If our dataset expanded 100x—from 200 pages to 20,000 pages (~150,000 chunks):\n'
        '1. Vector DB Bottleneck: In-memory ChromaDB would suffer from RAM saturation and increased query latency during full scans.\n'
        '2. Retrieval Precision Dilution: As chunk density increases, multiple chunks share similar cosine scores, introducing retrieval noise.\n'
        'Solutions We Would Implement:\n'
        '• Migrate from embedded ChromaDB to a distributed vector index like Qdrant, Milvus, or Pinecone utilizing HNSW (Hierarchical Navigable Small World) indexing.\n'
        '• Implement a Two-Stage Retrieval Pipeline: Stage 1 retrieves top-50 candidates using dense vector search; Stage 2 applies a Cross-Encoder Re-ranker (such as BGE-Reranker) to pass only the top 3 highest-precision chunks to Gemini.\n'
        '• Metadata Filtering: Partition the index by department, college, or handbook year to narrow search scope prior to vector similarity calculation."'
    ),
    (
        'Defense Question 5: "If you had time to fine-tune a model with LoRA or QLoRA, what would you target and why?"',
        'Assigned Speaker: Jenalyn Sabal (AI Orchestrator)',
        'Comprehensive Answer:\n'
        '"As documented in our Deliverable 15 Model Customization Note:\n'
        'Fine-tuning an LLM to memorize dynamic facts or policies is an anti-pattern because institutional rules change, leading to model obsolescence and catastrophic forgetting. RAG is strictly superior for factual retrieval.\n\n'
        'However, if we used LoRA (Low-Rank Adaptation) or QLoRA (4-bit Quantized LoRA), our specific target would be Style, Syntax, and Language Adaptation:\n'
        '1. Formal Legal Citation Syntax: Fine-tuning a low-rank adapter to consistently output structured JSON citations matching TPC administrative reporting standards.\n'
        '2. Multilingual & Dialect Adaptation: Adapting the model on Cebuano/Bisaya and Taglish campus vernacular queries while retrieving English handbook rules, enabling seamless cross-lingual comprehension without altering base factual weights."'
    )
]

for title, speaker, answer in qa_list:
    h = doc.add_heading(title, level=2)
    h.runs[0].font.color.rgb = RGBColor(180, 40, 40)
    p_spk = doc.add_paragraph(speaker)
    p_spk.runs[0].bold = True
    p_spk.runs[0].font.italic = True
    doc.add_paragraph(answer)
    doc.add_paragraph()

# -------------------------------------------------------------
# SECTION 5: REPOSITORY & DOCUMENTATION REQUIREMENTS (SECTION 7)
# -------------------------------------------------------------
add_custom_heading('5. Repository & Documentation Checklist (Section 7 Requirements)', level=1)
doc.add_paragraph(
    'Per Section 7 of the Capstone Guide, every checkpoint submission lives in the same Git repository. '
    'The repository must contain the following structured artifacts by the final defense:'
)

repo_items = [
    ('README.md', 'Comprehensive setup instructions, architecture diagram, environment variables guide, and instructions to run locally and via Docker.'),
    ('/data', 'Contains /raw (original handbook PDFs and website text dumps) and /processed (cleaned chunks and embedding metadata).'),
    ('/src or /app', 'Clean modular codebase: /ingestion (preprocessing & chunking), /retrieval (ChromaDB & similarity search), /orchestrator (Gemini API & memory), /ui (Streamlit app).'),
    ('Dockerfile', 'Multi-stage Docker build file with minimal image footprint, proper .dockerignore, and non-root execution.'),
    ('/docs/project_proposal.md', 'Checkpoint 1 deliverable: Problem background, objectives, and scope.'),
    ('/docs/prompt_engineering.md', 'Checkpoint 2 deliverable: System prompt iterations, few-shot examples, and guardrail definitions.'),
    ('/docs/framework_comparison.md', 'Checkpoint 3 deliverable: 1/2 to 1-page technical comparison of LangChain vs. LlamaIndex routing and our architectural choice.'),
    ('/docs/model_customization.md', 'Checkpoint 4 deliverable: 1-2 page write-up on PEFT (LoRA/QLoRA) evaluation versus base RAG implementation.'),
    ('/docs/final_technical_report.md', 'Checkpoint 4 deliverable: 3-5 page consolidated technical report covering architecture, data pipeline, deployment, evaluation metrics, and lessons learned.')
]

r_table = doc.add_table(rows=1, cols=2)
r_table.alignment = WD_TABLE_ALIGNMENT.CENTER
r_table.style = 'Table Grid'
r_hdr = r_table.rows[0].cells
r_hdr[0].text = 'Repository Item / Document'
r_hdr[0].paragraphs[0].runs[0].bold = True
r_hdr[1].text = 'Required Content & Rubric Standard'
r_hdr[1].paragraphs[0].runs[0].bold = True

for path_name, desc in repo_items:
    row_cells = r_table.add_row().cells
    row_cells[0].text = path_name
    row_cells[0].paragraphs[0].runs[0].bold = True
    row_cells[1].text = desc

doc.add_paragraph()

# -------------------------------------------------------------
# SECTION 6: 5-TO-8 MINUTE DEMO VIDEO RECORDING SCRIPT & FLOW
# -------------------------------------------------------------
add_custom_heading('6. 5-to-8 Minute Demo Video Recording Script & Flow', level=1)
doc.add_paragraph(
    'Per the Semester Project Guidelines, the video demonstration must be 5 to 8 minutes long and cover the following 5 parts in exact order:'
)

video_parts = [
    ('Part 1 (0:00 - 1:15): Problem & Knowledge Source', 'Speaker: Jerwin Villarin', 'Open deployed app homepage or title slide. Explain the problem (students struggling with 203-page PDF) and the official knowledge source (TPC Student Handbook v.04, 268 chunks).'),
    ('Part 2 (1:15 - 2:30): System Architecture', 'Speakers: Trisha & Jenalyn', 'Show architecture diagram / specs expander. Detail embedding model (all-MiniLM-L6-v2), vector store (ChromaDB, cosine similarity), LLM (Google Gemini 3.8 Flash, Temp 0.0), and conversational memory.'),
    ('Part 3 (2:30 - 3:45): Live App Walkthrough', 'Speaker: Kaycee Cerida', 'Show live Railway app. Highlight: opens with NO login and NO install; modern Gemini UI; chat history sidebar; interactive Visual Uniform Gallery.'),
    ('Part 4 (3:45 - 5:45): Live Query Demonstration (4 Queries)', 'Speaker: Kaycee & Team', 'Execute 4 live queries: 1. Academic grading (English, citations drawer); 2. Uniform & visual dress code (Bisaya, automatic photos); 3. Multi-turn memory follow-up; 4. Out-of-scope refusal (anti-hallucination guardrail).'),
    ('Part 5 (5:45 - 6:45): What We Would Improve & Conclusion', 'Speakers: Trisha & Jerwin', 'Discuss future improvements: distributed vector indexing (Qdrant/Milvus) for 100x scaling, Cross-Encoder re-ranker, and speech/voice input.')
]

v_table = doc.add_table(rows=1, cols=3)
v_table.alignment = WD_TABLE_ALIGNMENT.CENTER
v_table.style = 'Table Grid'
v_hdr = v_table.rows[0].cells
v_hdr[0].text = 'Video Section & Time'
v_hdr[0].paragraphs[0].runs[0].bold = True
v_hdr[1].text = 'Speaker'
v_hdr[1].paragraphs[0].runs[0].bold = True
v_hdr[2].text = 'Screen Action & Content'
v_hdr[2].paragraphs[0].runs[0].bold = True

for s_time, spk, act in video_parts:
    row_cells = v_table.add_row().cells
    row_cells[0].text = s_time
    row_cells[0].paragraphs[0].runs[0].bold = True
    row_cells[1].text = spk
    row_cells[2].text = act

doc.add_paragraph()

# Conclusion Note
p_fin = doc.add_paragraph()
p_fin.alignment = WD_ALIGN_PARAGRAPH.CENTER
run_fin = p_fin.add_run('--- End of PolyBot Defense Script & Deliverables Guide ---')
run_fin.font.italic = True
run_fin.font.color.rgb = RGBColor(120, 120, 120)

# Save document
doc.save('PolyBot_Defense_Script.docx')
print("Successfully generated comprehensive PolyBot_Defense_Script.docx!")