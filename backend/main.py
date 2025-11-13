import os
import re
import requests
import chromadb
from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Always load .env from the same folder as this file
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

# --------------------------
# FastAPI setup
# --------------------------
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------
# ChromaDB setup (fully portable)
# --------------------------
BASE_DIR = Path(__file__).resolve().parent
persist_path = BASE_DIR / "chromadb_store"
persist_path.mkdir(exist_ok=True)

print(f"📂 Using persistent ChromaDB path: {persist_path}")

chroma_client = chromadb.PersistentClient(path=str(persist_path))
collection = chroma_client.get_or_create_collection("partselect_parts")

embedder = SentenceTransformer("all-MiniLM-L6-v2")

# --------------------------
# DeepSeek setup
# --------------------------
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
if not DEEPSEEK_API_KEY:
    print("⚠️ DEEPSEEK_API_KEY not found in environment. Add it to your .env file.")

DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"

# --------------------------
# Request schema
# --------------------------
class ChatRequest(BaseModel):
    query: str

# --------------------------
# Utility rules
# --------------------------

def extract_part_number(text: str):
    """Extract PS12345678 style part numbers."""
    match = re.search(r"\bPS\d+\b", text.upper())
    return match.group(0) if match else None

def is_greeting(text: str):
    greetings = {"hi", "hello", "hey", "thanks", "thank you"}
    return text.lower().strip() in greetings

def is_out_of_scope(text: str):
    allowed_keywords = [
        "refrigerator", "fridge", "freezer", "ice", "dishwasher",
        "rack", "gasket", "hinge", "valve", "thermostat", "shelf",
        "bin", "pan", "pump", "sensor"
    ]
    return not any(keyword in text.lower() for keyword in allowed_keywords)

# --------------------------
# Chat endpoint
# --------------------------
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    user_query = request.query.strip()

    print("\n=======================")
    print("🗣️ USER QUERY:", user_query)

    # 1️⃣ Greetings
    if is_greeting(user_query):
        return {"message": "Hello! How can I help you with refrigerator or dishwasher parts today?"}

    # 2️⃣ Check out-of-scope
    part_number = extract_part_number(user_query)
    if not part_number and is_out_of_scope(user_query):
        return {"message": "I can assist only with refrigerator and dishwasher parts. Please ask a relevant question!"}

    # --------------------------
    # 3️⃣ Retrieval Logic (Exact Match → Semantic)
    # --------------------------
    results = None
    exact_hit = False

    if part_number:
        direct = collection.get(where={"part_number": {"$eq": part_number}})
        if direct and direct.get("ids"):
            exact_hit = True
            print(f"✅ Exact match found for {part_number}")

            results = {
                "ids": [[direct["ids"][0]]],
                "metadatas": [[direct["metadatas"][0]]],
                "documents": [[direct["documents"][0]]],
            }
        else:
            print(f"⚠️ No exact match for {part_number}. Falling back to semantic search.")

    if results is None:
        embedding = embedder.encode(user_query).tolist()
        results = collection.query(query_embeddings=[embedding], n_results=3)
        print("🧠 Using semantic search")

    # --------------------------
    # 4️⃣ Build Context
    # --------------------------
    contexts = []
    for i in range(len(results["ids"][0])):
        meta = results["metadatas"][0][i]
        desc = results["documents"][0][i]
        contexts.append(
            f"• {meta['title']} ({meta['category']}, part {meta['part_number']}): {desc}"
        )

    context_text = "\n".join(contexts) if contexts else "No relevant parts found."

    print("\n🧠 FINAL CONTEXT SENT TO LLM:\n", context_text)

    # --------------------------
    # 5️⃣ LLM Prompt (Strict RAG)
    # --------------------------
    prefix = ""
    if exact_hit and part_number:
        prefix = f"✅ I found an exact match for part number {part_number}.\n\n"

    messages = [
        {
            "role": "system",
            "content": (
                "You are the PartSelect AI assistant. "
                "You MUST answer ONLY using the provided part context. "
                "If the part exists in context, describe it accurately. "
                "If not in context, say: 'No matching part found.' "
                "NEVER invent part numbers, features, brands, or models."
            )
        },
        {
            "role": "user",
            "content": (
                f"CONTEXT:\n{context_text}\n\n"
                f"USER QUESTION:\n{user_query}"
            )
        }
    ]

    payload = {
        "model": "deepseek-chat",
        "messages": messages,
    }

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }

    # --------------------------
    # 6️⃣ Send to DeepSeek
    # --------------------------
    try:
        r = requests.post(
            DEEPSEEK_URL,
            headers=headers,
            json=payload,
            timeout=90,
        )
        data = r.json()
        print("🔍 DeepSeek raw response:", data)

        if "choices" in data:
            reply = data["choices"][0]["message"]["content"]
            return {"message": prefix + reply}

        elif "error" in data:
            return {"message": f"DeepSeek error: {data['error']}"}

        else:
            return {"message": f"Unexpected response: {data}"}

    except Exception as e:
        print("❌ Exception:", e)
        return {"message": f"Backend error: {str(e)}"}
