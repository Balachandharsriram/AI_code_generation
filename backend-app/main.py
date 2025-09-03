# ====================================================================
# SECTION 1: IMPORTS
# All the necessary libraries for our application.
# ====================================================================
import google.generativeai as genai
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import chromadb
from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session
from database import SessionLocal, create_db_tables, Generation


# ====================================================================
# SECTION 2: API & RAG SETUP
# Initializes the AI model, FastAPI app, and our RAG system.
# ====================================================================

# Configure the Gemini AI model with your API key.
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Initialize the ChromaDB client and the embedding model for RAG.
chroma_client = chromadb.Client()
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Get the knowledge base collection.
try:
    kb_collection = chroma_client.get_collection(name="plc_knowledge")
except Exception as e:
    print(f"Warning: Knowledge base not found. Please run create_kb.py first. Error: {e}")
    kb_collection = None

# Initialize the FastAPI application.
app = FastAPI()

# Add CORS middleware to allow the frontend to communicate with the backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Call the function to create the database tables on startup.
create_db_tables()


# ====================================================================
# SECTION 3: RAG LOGIC & UTILITY
# A helper function to get relevant context from our knowledge base.
# ====================================================================
def get_relevant_docs(query, k=2):
    """Searches the knowledge base for relevant documents based on a query."""
    if not kb_collection:
        return ""
    
    query_embedding = embedding_model.encode(query).tolist()
    
    results = kb_collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )
    
    relevant_docs = "\n".join(results['documents'][0])
    return relevant_docs


# ====================================================================
# SECTION 4: CODE VALIDATOR
# A basic validator to check for common Structured Text syntax errors.
# ====================================================================
def validate_st_code(code: str) -> dict:
    """A basic validator for Structured Text code."""
    errors = []
    warnings = []

    if 'IF' in code and 'END_IF' not in code:
        errors.append("Unclosed 'IF' statement. Missing 'END_IF;'.")
    if 'FOR' in code and 'END_FOR' not in code:
        errors.append("Unclosed 'FOR' loop. Missing 'END_FOR;'.")
    
    lines = code.strip().split('\n')
    for line in lines:
        if line.strip() and not line.strip().endswith(';') and not line.strip().startswith('//'):
            warnings.append(f"Line might be missing a semicolon at the end: '{line.strip()}'")

    return {"is_valid": len(errors) == 0, "errors": errors, "warnings": warnings}


# ====================================================================
# SECTION 5: API ENDPOINTS
# The main logic for our application's API.
# ====================================================================

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/generate_st")
async def generate_st(request: Request):
    """Generates Structured Text code and validates it."""
    data = await request.json()
    description = data.get("description", "")
    db = SessionLocal()
    
    try:
        context = get_relevant_docs(description)
        
        prompt = f"""
        You are a PLC programming assistant. Your task is to generate a complete and well-structured PLC Structured Text (ST) code snippet based on a natural language description.
        
        The generated code must follow these rules:
        1. Include a 'VAR' section with comments for each variable.
        2. Use clear, descriptive variable names.
        3. Include detailed comments ('//' style) throughout the logic section to explain the process.
        4. The output must be a complete, ready-to-use code block. Do not include any extra text or explanations outside of the code.

        Use the following additional context to inform your response:
        ---
        {context}
        ---
        
        Description to convert to ST code:
        {description}
        """
        response = model.generate_content(prompt)
        generated_content = response.text
        
        validation_results = validate_st_code(generated_content)
        
        # Save the generation to the database.
        db_generation = Generation(
            description=description,
            st_code=generated_content,
            is_valid=validation_results["is_valid"]
        )
        db.add(db_generation)
        db.commit()

        print("Generated ST Content from AI:")
        print(generated_content)
        
        return {
            "code": generated_content,
            "validation": validation_results
        }
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}
    finally:
        db.close()


@app.post("/generate_ld")
async def generate_ld(request: Request):
    """Generates Ladder Diagram."""
    data = await request.json()
    description = data.get("description", "")
    db = SessionLocal()

    try:
        context = get_relevant_docs(description)

        prompt = f"""
        You are a PLC programming assistant. Your task is to generate a Ladder Diagram based on a natural language description.

        The Ladder Diagram must follow this exact schema:
        - An array of 'rungs'.
        - Each 'rung' is an object with a unique 'id' and an array of 'elements'.
        - Each 'element' is an object with a 'type' (e.g., 'contact_NO', 'contact_NC', 'coil') and a 'tag' (e.g., 'Start_PB', 'Motor_1').
        - Only output the Ladder diagram. Do not include any extra text, explanations.

        Use the following additional context to inform your response:
        ---
        {context}
        ---
        Description to convert to Ladder Diagram:
        {description}
        """
        response = model.generate_content(prompt)
        generated_content = response.text
        
        db_generation = Generation(
            description=description,
            ld_json=generated_content
        )
        db.add(db_generation)
        db.commit()
        
        print("Generated LD from AI:")
        print(generated_content)
        
        return {"code": generated_content}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}
    finally:
        db.close()