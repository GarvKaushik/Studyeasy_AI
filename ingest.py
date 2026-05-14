from src.data_loader import (
    process_all_pdfs,
    split_documents
)

from src.embeddings import EmbeddingManager

from src.vectorstore import VectorStore


def run_ingestion():

    print("Starting document ingestion...")

    # Load documents
    docs = process_all_pdfs("data/text_files")

    # Split documents
    chunks = split_documents(docs)

    print(f"Total chunks created: {len(chunks)}")

    # Generate embeddings
    embedding_manager = EmbeddingManager()

    embeddings = embedding_manager.generate_embeddings(
        [doc.page_content for doc in chunks]
    )

    # Store embeddings
    vector_store = VectorStore()

    vector_store.add_documents(
        chunks,
        embeddings
    )

    print("Ingestion completed successfully.")


if __name__ == "__main__":
    run_ingestion()