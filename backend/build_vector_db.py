# build_vector_db.py
import os
import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer
# ---------------------------
# Persistent Chroma setup
# ---------------------------
from pathlib import Path

# Dynamically resolve the backend folder
BASE_DIR = Path(__file__).resolve().parent
persist_path = str(BASE_DIR / "chromadb_store")

# Create the folder if it doesn't exist
os.makedirs(persist_path, exist_ok=True)
print(f"📂 Using persistent path: {persist_path}")


# ✅ Persistent Chroma client (v1.3.4+)
client = chromadb.PersistentClient(path=persist_path)

# ---------------------------
# Load CSV and model
# ---------------------------
csv_path = "partselect_products.csv"
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"❌ CSV file not found: {csv_path}")

df = pd.read_csv(csv_path)
print(f"📄 Loaded {len(df)} products from CSV")

model = SentenceTransformer("all-MiniLM-L6-v2")

# ---------------------------
# Create collection
# ---------------------------
collection_name = "partselect_parts"
collection = client.get_or_create_collection(name=collection_name)
print(f"🧩 Using collection: {collection_name}")

# ✅ Clear existing records safely (compatible with Chroma ≥1.3)
existing_count = collection.count()
if existing_count > 0:
    existing = collection.get(limit=existing_count)
    if "ids" in existing and existing["ids"]:
        collection.delete(ids=existing["ids"])
        print(f"🧹 Cleared {len(existing['ids'])} old embeddings")

# ---------------------------
# Embed and store records
# ---------------------------
print(f"🧠 Embedding {len(df)} parts...")

for _, row in df.iterrows():
    desc = str(row["description"])
    embedding = model.encode(desc).tolist()

    collection.add(
        ids=[row["part_number"]],
        embeddings=[embedding],
        metadatas=[{
            "category": row["category"],
            "title": row["title"],
            "url": row.get("url", ""),
            "part_number": row["part_number"],  # ✅ added for direct ID lookup
        }],
        documents=[desc],
    )


print("✅ All embeddings stored and persisted successfully!")
print(f"📊 Total records now: {collection.count()}")
