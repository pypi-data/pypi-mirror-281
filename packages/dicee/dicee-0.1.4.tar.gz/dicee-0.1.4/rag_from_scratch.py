import requests
import json
import ast
print("CHAT STREAM")
for i in requests.get(url="http://diceemb.cs.upb.de:8000/api/chat",
                      headers={"accept": "application/json", "Content-Type": "application/json"},
                      json={"key": 84,
                            "model": "mixtral:8x7b",
                            "messages": [
                                {"role": "user", "content": "why is the sky blue?"}],
                            "stream": True}, stream=True).iter_lines(decode_unicode=True):
    print(json.loads(i.decode("utf-8")))


print("CHAT without STREAM")
print(requests.get(url="http://diceemb.cs.upb.de:8000/api/chat",
                   headers={"accept": "application/json", "Content-Type": "application/json"},
                   json={"key": 84,
                         "model": "mixtral:8x7b",
                         "messages": [
                             {"role": "user", "content": "why is the sky blue?"}]},
                   stream=False).json())

print("GENERATE without Stream")
print(requests.get(url="http://diceemb.cs.upb.de:8000/api/generate",
                   headers={"accept": "application/json", "Content-Type": "application/json"},
                   json={"key": 84,
                         "model": "mixtral:8x7b",  # or llama2:70b
                         "prompt": "Why is the sky blue ?"}, stream=False).json()["response"])

print("GENERATE STREAM")
for i in requests.get(url="http://diceemb.cs.upb.de:8000/api/generate",
                      headers={"accept": "application/json", "Content-Type": "application/json"},
                      json={"key": 84,
                            "model": "mixtral:8x7b",  # or llama2:70b
                            "prompt": "Why is the sky blue ?", "stream": True}, stream=True).iter_lines(decode_unicode=True):
    print(json.loads(i.decode("utf-8")))

exit(1)

exit(1)
# https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt
import pickle

import numpy as np
import requests
import asyncio


def get_embeddings(x):
    embedding_vector = np.array(requests.get(url="http://diceemb.cs.upb.de:8000/api/embeddings",
                                             headers={"accept": "application/json", "Content-Type": "application/json"},
                                             json={"key": 84,
                                                   "model": "mixtral:8x7b",  # or llama2:70b
                                                   "prompt": x}).json()["embedding"])
    return embedding_vector  # / np.linalg.norm(embedding_vector)


def async_get_embeddings(docs):
    async def process_item(item):
        # Simulate processing time
        return requests.get(url="http://diceemb.cs.upb.de:8000/api/embeddings",
                            headers={"accept": "application/json", "Content-Type": "application/json"},
                            json={"key": 84,
                                  "model": "mixtral:8x7b",
                                  "prompt": item}).json()["embedding"]

    async def process_items(items):
        # Create tasks for processing each item concurrently
        tasks = [process_item(item) for item in items]
        # Wait for all tasks to complete
        return await asyncio.gather(*tasks)

    async def main(items):
        return await process_items(items)

    # Run the main coroutine
    return asyncio.run(main(docs))


def topk_indices(arr, k):
    # Get the indices that would sort the array in descending order
    sorted_indices = np.argsort(arr)[::-1]
    # Slice to get the top k indices
    return sorted_indices[:k]


indexxing = False

if indexxing:
    documents = []
    # Reading
    with open("/home/demir/Desktop/paul_graham_essay.txt") as r:
        for it, line in enumerate(r.readlines()):
            # Poor man's preprocessing
            if len(line) <= 1:
                continue
            documents.append(line)

    document_embeddings = []
    print("Indexing...")
    vector_db = np.array(async_get_embeddings(documents))
    print(len(documents))
    print(vector_db.shape)
    with open("names.list", "wb") as f:
        pickle.dump(documents, f)
    with open("vector_db.npy", "wb") as f:
        np.save(f, vector_db)
else:
    with open("names.list", "rb") as f:
        documents = pickle.load(f)
    with open("vector_db.npy", "rb") as f:
        vector_db = np.load(f)
    # A sentence in a document Meanwhile I was applying to art schools
    text = "IBM"
    print("USER:", text)
    scores = vector_db @ get_embeddings(text)
    top_indices = topk_indices(scores, k=3)
    for i in top_indices:
        print(documents[i])

    # idx = np.argmax(vector_db @ get_embeddings(text))
    # print(scores[idx])
    # print(idx)
    # print("Answer:", documents[idx])
