from document_loader import load_all_pdfs


def create_chunks(
    documents,
    chunk_size=500,
    overlap=100
):

    chunks = []

    for document in documents:

        text = document["text"]
        source = document["source"]
        page = document["page"]
        company = document["company"]

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk_text = text[
                start:end
            ].strip()

            if chunk_text:

                chunks.append({
                    "text": chunk_text,
                    "source": source,
                    "page": page,
                    "company": company
                })

            start += (
                chunk_size - overlap
            )

    return chunks


if __name__ == "__main__":

    documents = load_all_pdfs()

    chunks = create_chunks(documents)

    print(
        f"Created {len(chunks)} chunks."
    )

    print("\n===== FIRST CHUNK =====")

    if chunks:

        print(
            chunks[0]["text"]
        )

        print(
            "Company:",
            chunks[0]["company"]
        )

        print(
            "Source:",
            chunks[0]["source"]
        )

        print(
            "Page:",
            chunks[0]["page"]
        )