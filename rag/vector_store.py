from sentence_transformers import SentenceTransformer
import chromadb

from document_loader import load_all_pdfs
from chunker import create_chunks


def build_vector_store():

    # Load documents
    documents = load_all_pdfs()

    print(f"\nLoaded {len(documents)} readable pages.")

    # Create chunks
    chunks = create_chunks(documents)

    print(f"Created {len(chunks)} chunks.")

    # Load embedding model
    print("\nLoading embedding model...")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Embedding model loaded.")

    # ChromaDB
    client = chromadb.PersistentClient(
        path="rag/chroma_db"
    )

    try:
        client.delete_collection(
            "financial_documents"
        )
    except Exception:
        pass

    collection = client.create_collection(
        name="financial_documents"
    )

    # Prepare all text
    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    print(
        f"\nCreating embeddings in batches..."
    )

    # BATCH EMBEDDING
    embeddings = model.encode(
        texts,
        batch_size=100,
        show_progress_bar=True
    )

    # Store in ChromaDB in batches
    batch_size = 100

    for start in range(
        0,
        len(chunks),
        batch_size
    ):

        end = min(
            start + batch_size,
            len(chunks)
        )

        batch_chunks = chunks[start:end]
        batch_embeddings = embeddings[start:end]

        collection.add(

            ids=[
                str(i)
                for i in range(start, end)
            ],

            embeddings=[
                embedding.tolist()
                for embedding in batch_embeddings
            ],

            documents=[
                chunk["text"]
                for chunk in batch_chunks
            ],

            metadatas=[
                {
                    "source": chunk["source"],
                    "page": chunk["page"],
                    "company": chunk["company"]
                }
                for chunk in batch_chunks
            ]
        )

    print(
        f"\nStored {len(chunks)} chunks in ChromaDB."
    )

    print(
        "\n===== VECTOR STORE READY ====="
    )


if __name__ == "__main__":

    build_vector_store()