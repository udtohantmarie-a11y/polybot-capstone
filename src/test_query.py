import os
import torch
from transformers import AutoTokenizer, AutoModel
import chromadb

def embed_query(text, model_name='sentence-transformers/all-MiniLM-L6-v2'):
    """Generates an embedding for the query using the exact same model from generate_embeddings.py"""
    print(f"Loading Hugging Face model for query: {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    
    inputs = tokenizer([text], padding=True, truncation=True, return_tensors="pt", max_length=512)
    
    with torch.no_grad():
        outputs = model(**inputs)
        
    # Mean pooling
    attention_mask = inputs['attention_mask']
    token_embeddings = outputs[0]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
    sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    embeddings = sum_embeddings / sum_mask
    
    return embeddings.tolist()

def main():
    # Use absolute paths based on the script's location
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, 'data', 'chroma_db')

    print("Connecting to ChromaDB...")
    client = chromadb.PersistentClient(path=db_path)
    
    # Get the existing collection
    collection = client.get_collection(name='tpc_student_handbook')

    print(f"Collection loaded. Total documents: {collection.count()}")

    # A sample user query
    query_text = "What is the policy on wearing school uniforms and dress code?"
    print(f"\nSearching for: '{query_text}'")

    # FIX: Generate embedding for the query manually to bypass Chroma's default downloader
    query_embedding = embed_query(query_text)

    # Perform the similarity search using the generated embedding directly
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=2 # Retrieve top 2 most similar chunks
    )

    print("\n--- Similarity Search Results ---")
    for i in range(len(results['documents'][0])):
        distance = results['distances'][0][i]
        document = results['documents'][0][i]
        metadata = results['metadatas'][0][i]
        
        print(f"\nResult {i+1} (Distance: {distance:.4f}):")
        print(f"Source: {metadata['source']}")
        print(f"Text: {document}")

if __name__ == "__main__":
    main()