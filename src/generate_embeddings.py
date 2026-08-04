import os
import torch
from transformers import AutoTokenizer, AutoModel

def load_cleaned_text(file_path):
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found. Please run preprocess.py first.")
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
    text_path = "../data/cleaned_handbook.txt"
    
    print("Reading cleaned handbook text...")
    text = load_cleaned_text(text_path)
    
    if not text:
        return

    print("Chunking text...")
    chunks = chunk_text(text, chunk_size=150)
    print(f"Total chunks created: {len(chunks)}")
    
    # Let's take a sample of the first 5 chunks for the demo script
    sample_chunks = chunks[:5]
    
    inputs, embeddings = generate_embeddings(sample_chunks)
    
    print("\n--- Embedding Generation Results ---")
    print("Input IDs Shape:", inputs['input_ids'].shape)
    print("Attention Mask Shape:", inputs['attention_mask'].shape)
    print("Generated Embeddings Shape:", embeddings.shape)
    print("Embedding generation demo completed successfully!")

if __name__ == "__main__":
    main()