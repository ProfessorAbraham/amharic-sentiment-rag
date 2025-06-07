
import os
import json
import torch
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

device = 'cuda' if torch.cuda.is_available() else 'cpu'

model = SentenceTransformer("intfloat/multilingual-e5-large")
model.to(device)

def embed_texts(texts, batch_size=32):
    embeddings = []
    for i in tqdm(range(0, len(texts), batch_size)):
        batch = texts[i:i+batch_size]
        emb = model.encode(batch, convert_to_numpy=True)
        embeddings.extend(emb)
    return embeddings

def embed_cleaned_comments(input_folder="comments_data", output_folder="embeddings"):
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith("_cleaned.json"):
            input_path = os.path.join(input_folder, filename)
            with open(input_path, 'r', encoding='utf-8') as f:
                comments = json.load(f)

            texts = [c["text"] for c in comments]
            embeddings = embed_texts(texts)

            output_data = [
                {"text": text, "embedding": emb.tolist()}
                for text, emb in zip(texts, embeddings)
            ]

            output_path = os.path.join(output_folder, filename.replace("_cleaned.json", "_embedded.json"))
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)

            print(f"Embedded {filename} -> {output_path}")

if __name__ == "__main__":
    embed_cleaned_comments()
