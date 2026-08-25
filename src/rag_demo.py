import os
import chromadb
import torch
from transformers import AutoTokenizer, AutoModel
from dotenv import load_dotenv
from google import genai
from google.genai import types

def embed_query(text, model_name='sentence-transformers/all-MiniLM-L6-v2'):
    """Generates an embedding for the query."""
    print(f"Loading Hugging Face model for query...")
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
    # Load environment variables from .env file securely
    load_dotenv()
    
    # Use absolute paths based on the script's location
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, 'data', 'chroma_db')

    print("Connecting to ChromaDB...")
    chroma_client = chromadb.PersistentClient(path=db_path)
    collection = chroma_client.get_collection(name='tpc_student_handbook')

    # The user's question optimized for better retrieval of Chapter 6
    user_query = "What is the grading system rating and description equivalent in Chapter 6?"
    print(f"\nUser Query: '{user_query}'")

    # 1. Retrieve relevant context from ChromaDB (Increased n_results to capture the rating table)
    query_embedding = embed_query(user_query)
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=6 # Increased from 3 to 6 to grab more surrounding context blocks
    )
    
    # Combine the retrieved chunks into a single context string
    retrieved_context = "\n\n".join(results['documents'][0])
    print("\n--- Retrieved Context from Database ---")
    print(retrieved_context)

    # 2. Initialize Gemini API Client
    print("\nConnecting to Gemini API...")
    # The client automatically picks up the GEMINI_API_KEY from the .env file
    gemini_client = genai.Client() 
    
    # 3. Create the Prompt Architecture (System Instruction)
    system_instruction = (
        "You are PolyBot, a helpful and accurate Campus Tourism & History Guide for Talibon Polytechnic College (TPC). "
        "Answer the user's question using ONLY the information provided in the context below. "
        "If the answer cannot be found in the context, respond exactly with: 'I don't have enough information to answer that based on the handbook.' "
        "Do not use any outside knowledge. Always cite the relevant Article or Chapter if available in the context."
    )

    # 4. Generate the response
    print("Generating grounded response...")
    response = gemini_client.models.generate_content(
        model='gemini-3.6-flash',
        contents=f"<context>\n{retrieved_context}\n</context>\n\nQuestion: {user_query}",
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.0 # Low temperature for factual, deterministic answers
        )
    )

    print("\n--- PolyBot's Final Answer ---")
    print(response.text)

if __name__ == "__main__":
    main()