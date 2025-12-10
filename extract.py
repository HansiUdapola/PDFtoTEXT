import os
import pdfplumber

# This script will be useful if someone have pdf and need to extract data from it 
# and save it as text file. 
# USE CASE 1: To upload in server as knowledge base rather uploading pdf/docx files.

# === CONFIG ===
PDF_FOLDER = "./PDF"         # change this to your folder
OUTPUT_FILE = "./knowledge_base.txt"

# If need to add a title for the knowledge base based on the pdf file to reflect its major type of the content.
# Better if have one pdf file for each content type.
DOC_CONTENT_TYPE_OVERRIDES = {
    # "PDF_NAME.pdf": "Readable Name For the PDF File",
    "FeePayingSV.pdf" : "Fee Paying Student Visa in NZ"
}

def guess_pdf_content_type(filename: str) -> str:
    """Return a pdf file's content type label based on filename or override table."""
    base = os.path.basename(filename)
    if base in DOC_CONTENT_TYPE_OVERRIDES:
        return DOC_CONTENT_TYPE_OVERRIDES[base]

    name = os.path.splitext(base)[0].replace("_", " ").replace("-", " ")
    return name.title()  # e.g. "student_visa" -> "Student Visa"

def extract_text_from_pdf(path: str) -> str:
    """Extract text from all pages of a PDF using pdfplumber."""
    parts = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            parts.append(text.strip())
    # Join pages with two newlines to keep some separation
    return "\n\n".join(p for p in parts if p)

def main():
    pdf_files = [
        os.path.join(PDF_FOLDER, f)
        for f in os.listdir(PDF_FOLDER)
        if f.lower().endswith(".pdf")
    ]

    if not pdf_files:
        print("No PDF files found in:", PDF_FOLDER)
        return

    combined_chunks = []

    for pdf_path in sorted(pdf_files):
        filename = os.path.basename(pdf_path)
        content_type = guess_pdf_content_type(filename)
        print(f"Processing: {filename}  (Content type: {content_type})")

        text = extract_text_from_pdf(pdf_path)

        # Light cleaning
        cleaned = "\n".join(
            line.rstrip()
            for line in text.splitlines()
        ).strip()

        chunk = (
            "===== DOCUMENT START =====\n"
            f"[Source file]: {filename}\n"
            f"[Content type]: {content_type}\n\n"
            f"{cleaned}\n\n"
            "===== DOCUMENT END =====\n\n"
        )
        combined_chunks.append(chunk)

    combined_text = "".join(combined_chunks)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(combined_text)

    print("Done! Knowledge base written to:")
    print(OUTPUT_FILE)

if __name__ == "__main__":
    main()
