# create_kb.py
import chromadb
from sentence_transformers import SentenceTransformer
import os

# Initialize ChromaDB client and embedding model
chroma_client = chromadb.Client()
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Define the collection name
collection_name = "plc_knowledge"

# Check if collection exists and delete it to start fresh
try:
    chroma_client.delete_collection(name=collection_name)
    print(f"Deleted existing collection: {collection_name}")
except Exception:
    pass # No existing collection to delete

# Create a new collection
kb_collection = chroma_client.create_collection(name=collection_name)
print(f"Created new collection: {collection_name}")

# Directory containing your knowledge base text files
kb_dir = "knowledge_base"

# Ensure the directory exists
if not os.path.exists(kb_dir):
    print(f"Creating directory: {kb_dir}")
    os.makedirs(kb_dir)
    print(f"Please add your text files to the '{kb_dir}' directory and run the script again.")
else:
    print(f"Reading from directory: {kb_dir}")
    # Read all text from files in the directory
    documents = []
    ids = []
    file_list = [f for f in os.listdir(kb_dir) if f.endswith(".txt")]
    
    if not file_list:
        print("No text files found in the knowledge_base directory. Please add some.")
    else:
        for filename in file_list:
            filepath = os.path.join(kb_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
                # Split content into smaller, manageable chunks
                chunks = content.split('\n\n') 
                for i, chunk in enumerate(chunks):
                    if chunk.strip():
                        documents.append(chunk)
                        ids.append(f"{filename}-{i}")

        # Generate embeddings and add to the collection
        if documents:
            embeddings = embedding_model.encode(documents).tolist()
            kb_collection.add(
                documents=documents,
                embeddings=embeddings,
                ids=ids
            )
            print(f"Added {len(documents)} documents to the knowledge base.")