from pathlib import Path
from pypdf import PdfReader


def identify_company(filename):

    name = filename.lower()

    if "tcs" in name:
        return "TCS"

    if "infosys" in name:
        return "Infosys"

    if "reliance" in name or "ril" in name:
        return "Reliance"

    return "Unknown"


def load_pdf(file_path):

    reader = PdfReader(file_path)

    documents = []

    filename = Path(file_path).name
    company = identify_company(filename)

    for page_number, page in enumerate(reader.pages):

        text = page.extract_text()

        if text:

            documents.append({
                "text": text,
                "source": filename,
                "page": page_number + 1,
                "company": company
            })

    return documents


def load_all_pdfs(folder="documents"):

    all_documents = []

    pdf_files = list(
        Path(folder).glob("*.pdf")
    )

    print(f"Found {len(pdf_files)} PDF files.")

    for pdf_file in pdf_files:

        print(
            f"Loading: {pdf_file.name}"
        )

        documents = load_pdf(
            str(pdf_file)
        )

        all_documents.extend(documents)

    print(
        f"Loaded {len(all_documents)} pages total."
    )

    return all_documents


if __name__ == "__main__":

    documents = load_all_pdfs()

    print("\n===== DOCUMENT SUMMARY =====")

    companies = {}

    for document in documents:

        company = document["company"]

        companies[company] = (
            companies.get(company, 0) + 1
        )

    for company, count in companies.items():

        print(
            f"{company}: {count} pages"
        )