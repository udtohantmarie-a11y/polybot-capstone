import chromadb
import os

def initialize_chromadb():
    # Define the path for the persistent database inside the data folder
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, 'data', 'chroma_db')
    
    # Persistent client data is saved to disk between runs
    client = chromadb.PersistentClient(path=db_path)
    
    # Create (or get) a collection for the TPC handbook
    # ChromaDB embeds text automatically using a default sentence-transformer model unless you specify one
    collection = client.get_or_create_collection(name='tpc_student_handbook')
    
    print("ChromaDB vector database setup complete.")
    print(f"Database location: {db_path}")
    print(f"Current document count in collection: {collection.count()}")
    
    return collection

if __name__ == "__main__":
    collection = initialize_chromadb()