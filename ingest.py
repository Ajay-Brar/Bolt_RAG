import os
import uuid
from datetime import datetime
from dotenv import load_dotenv
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models.models import PDFMetadata, DocumentChunk

# 1. Load Environment Variables
load_dotenv()

# 2. Setup Database & AI
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
db: Session = SessionLocal()

def ingest_file(file_path):
    print(f"📄 Processing: {file_path}")
    
    # Read PDF
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    
    filename = os.path.basename(file_path)
    
    # Create PDF Metadata Entry in Postgres
    pdf_entry = PDFMetadata(
        filename=filename,
        source=filename,
        total_pages=len(reader.pages),
        embedding_dim=384
    )
    db.add(pdf_entry)
    db.commit()
    db.refresh(pdf_entry)

    # Chunking (Simple paragraph split for demo)
    # Ideally, use a recursive character splitter here
    chunks = [c for c in text.split('\n\n') if len(c) > 50]
    
    print(f"🧩 Split into {len(chunks)} chunks...")

    vectors = []
    
    for i, chunk_text in enumerate(chunks):
        # Generate ID
        chunk_id = str(uuid.uuid4())
        
        # Save to Postgres
        db_chunk = DocumentChunk(
            id=chunk_id,
            source=filename,
            text=chunk_text,
            page_number=1, # Simplified for demo
            pdf_metadata_id=pdf_entry.id
        )
        db.add(db_chunk)
        
        # Prepare for Pinecone
        embedding = model.encode(chunk_text).tolist()
        vectors.append({
            "id": chunk_id,
            "values": embedding,
            "metadata": {"source": filename}
        })

    db.commit()
    
    # Upload to Pinecone (Batching 100 at a time is better for large files)
    if vectors:
        index.upsert(vectors=vectors)
        print(f"✅ Successfully uploaded {len(vectors)} chunks to Pinecone!")
    else:
        print("⚠️ No text found in PDF to upload.")

if __name__ == "__main__":
    # Create a 'docs' folder if it doesn't exist
    if not os.path.exists("docs"):
        os.makedirs("docs")
        print("📁 Created 'docs' folder. Please put your PDFs there and run this again.")
    else:
        # Process all PDFs in the docs folder
        files = [f for f in os.listdir("docs") if f.endswith(".pdf")]
        if not files:
            print("⚠️ No PDFs found in 'docs/' folder.")
        for f in files:
            ingest_file(os.path.join("docs", f))