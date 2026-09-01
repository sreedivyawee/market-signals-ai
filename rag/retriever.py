from sentence_transformers import SentenceTransformer
import chromadb


def retrieve_documents(
    query,
    company=None,
    top_k=3
):

    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    client = chromadb.PersistentClient(
        path="rag/chroma_db"
    )

    collection = client.get_collection(
        name="financial_documents"
    )

    query_embedding = model.encode(
        query
    ).tolist()

    search_parameters = {
        "query_embeddings": [
            query_embedding
        ],
        "n_results": top_k
    }

    # Filter by company if supplied
    if company:

        search_parameters["where"] = {
            "company": company
        }

    results = collection.query(
        **search_parameters
    )

    retrieved_documents = []

    for i in range(
        len(results["documents"][0])
    ):

        retrieved_documents.append({

            "text":
                results["documents"][0][i],

            "source":
                results["metadatas"][0][i][
                    "source"
                ],

            "page":
                results["metadatas"][0][i][
                    "page"
                ],

            "company":
                results["metadatas"][0][i][
                    "company"
                ]
        })

    return retrieved_documents


if __name__ == "__main__":

    company = input(
        "Company (TCS/Infosys/Reliance): "
    )

    query = input(
        "Question: "
    )

    results = retrieve_documents(
        query=query,
        company=company,
        top_k=3
    )

    print(
        "\n===== RAG RESULTS ====="
    )

    for i, result in enumerate(
        results,
        start=1
    ):

        print(
            f"\n--- Result {i} ---"
        )

        print(
            "Company:",
            result["company"]
        )

        print(
            "Source:",
            result["source"]
        )

        print(
            "Page:",
            result["page"]
        )

        print(
            "Text:",
            result["text"][:500]
        )