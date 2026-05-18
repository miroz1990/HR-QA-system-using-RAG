from .metadata_utils import infer_role, extract_section
def chunk_text(text, chunk_size=300, overlap=50):
    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = words[start:end]
        chunks.append(" ".join(chunk))
        start += chunk_size - overlap

    return chunks


def chunk_documents(documents, chunk_size, overlap):
    all_chunks = []

    for doc in documents:
        chunks = chunk_text(doc["text"], chunk_size, overlap)

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "text": chunk,
                "source": doc["source"],

                # 🔥 NEW METADATA
                "chunk_id": i,
                "doc_type": doc["source"].replace(".txt", ""),

                # You can infer these or tag manually later
                "role": infer_role(doc["source"]),
                "section": extract_section(doc["text"]),
            })

    return all_chunks

