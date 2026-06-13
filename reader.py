import os
from pypdf import PdfReader

MATERIALS_DIR = os.environ.get("MATERIALS_DIR", os.path.expanduser("~/Documents/Materials"))

def read_pdf(filepath):
    reader = PdfReader(filepath)
    pages = []
    for page in reader.pages:
        text = page.extract_text()
        if text:               # some pages are images — skip them
            pages.append(text)
    return "\n".join(pages)

def read_text_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def load_all_materials(directory: str):
    documents = []

    for root, dirs, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(str(root), str(filename))
            label = os.path.relpath(filepath, str(directory))

            if filename.endswith(".pdf"):
                print(f"Reading PDF: {label}")
                text = read_pdf(filepath)
                documents.append({"filename": label, "text": text})

            elif filename.endswith((".md", ".txt")):
                print(f"Reading note: {label}")
                text = read_text_file(filepath)
                documents.append({"filename": label, "text": text})

    return documents


if __name__ == "__main__":
    docs = load_all_materials(MATERIALS_DIR)

    print(f"\n--- Loaded {len(docs)} documents ---\n")
    for doc in docs:
        preview = doc["text"][:300].replace("\n", " ")
        print(f"[{doc['filename']}] ({len(doc['text'])} chars)")
        print(f"  Preview: {preview}...")
        print()