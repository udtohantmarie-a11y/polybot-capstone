import os
import torch
from transformers import AutoTokenizer, AutoModel
import chromadb

def load_cleaned_text(file_path):
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found. Please ensure the file exists.")
        return ""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def chunk_text(text, chunk_size=150):
    # Split text into manageable chunks of words for embedding generation
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def generate_embeddings(text_chunks, model_name='sentence-transformers/all-MiniLM-L6-v2'):
    print(f"Loading Hugging Face model: {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    
    print("Tokenizing and generating embeddings...")
    inputs = tokenizer(text_chunks, padding=True, truncation=True, return_tensors="pt", max_length=512)
    
    with torch.no_grad():
        outputs = model(**inputs)
        
    # Mean pooling to get sentence/chunk level embeddings
    attention_mask = inputs['attention_mask']
    token_embeddings = outputs[0]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
    sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    embeddings = sum_embeddings / sum_mask
    
    return inputs, embeddings

def main():
    # Fix: Use absolute paths based on the script's location to prevent CWD errors
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    handbook_path = os.path.join(base_dir, 'data', 'cleaned_handbook.txt')
    website_path = os.path.join(base_dir, 'data', 'website_content.txt')
    db_path = os.path.join(base_dir, 'data', 'chroma_db')
    
    print("Reading handbook and website text...")
    handbook_text = load_cleaned_text(handbook_path)
    website_text = load_cleaned_text(website_path)
    
    if not handbook_text and not website_text:
        print("No data found to process.")
        return

    print("Chunking text...")
    handbook_chunks = chunk_text(handbook_text, chunk_size=150) if handbook_text else []
    website_chunks = chunk_text(website_text, chunk_size=150) if website_text else []
    
    all_chunks = handbook_chunks + website_chunks
    print(f"Total chunks created: {len(all_chunks)} ({len(handbook_chunks)} from handbook, {len(website_chunks)} from website)")
    
    if not all_chunks:
        return
        
    # Process all chunks for the database instead of just the sample
    inputs, embeddings = generate_embeddings(all_chunks)
    
    print("\n--- Embedding Generation Results ---")
    print("Input IDs Shape:", inputs['input_ids'].shape)
    print("Attention Mask Shape:", inputs['attention_mask'].shape)
    print("Generated Embeddings Shape:", embeddings.shape)
    
    # New Feature: ChromaDB Integration
    print("\nInitializing ChromaDB persistent storage...")
    
    client = chromadb.PersistentClient(path=db_path)
    collection = client.get_or_create_collection(name='tpc_student_handbook')
    
    print("Adding chunks and generated embeddings to ChromaDB...")
    # Convert PyTorch tensor to a list of lists of floats for ChromaDB
    embeddings_list = embeddings.tolist()
    
    # Generate unique IDs and metadata for each chunk based on source
    chunk_ids = []
    chunk_metadata = []
    
    for i in range(len(handbook_chunks)):
        chunk_ids.append(f"handbook_chunk_{i}")
        chunk_metadata.append({"source": "TPC Student Handbook v.04"})
        
    for i in range(len(website_chunks)):
        chunk_ids.append(f"website_chunk_{i}")
        chunk_metadata.append({"source": "TPC Official Website Compilation"})
    
    # Using upsert to prevent errors if the database already contains these IDs
    collection.upsert(
        documents=all_chunks,
        embeddings=embeddings_list,
        metadatas=chunk_metadata,
        ids=chunk_ids
    )
    
    print("\n--- ChromaDB Ingestion Results ---")
    print(f"Vector database populated successfully.")
    print(f"Database location: {db_path}")
    print(f"Total documents in collection: {collection.count()}")

if __name__ == "__main__":
    main()