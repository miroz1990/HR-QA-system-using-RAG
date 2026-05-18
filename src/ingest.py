import os

def load_documents(data_path="data/hr_docs"):
    documents = []

    for file in os.listdir(data_path):
        if file.endswith(".txt"):
            with open(os.path.join(data_path, file), "r") as f:
                text = f.read()

            documents.append({
                "text": text,
                "source": file
            })

    return documents