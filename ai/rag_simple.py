import faiss
from sentence_transformers import SentenceTransformer
from transformers import pipeline

texts = [
    "Atoms are the basic building blocks of matter.",
    "Mount Everest is the highest mountain in the world.",
    "Python is a popular programming language.",
    "Haiku is a traditional form of Japanese poetry.",
    "Transformers are powerful NLP models."
]

model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(texts)

index = faiss.IndexFlatL2(384)
index.add(embeddings)

qa = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")


def ask_question(query, k=2):
    query_vec = model.encode([query])
    _, results = index.search(query_vec, k=k)
    relevant = [texts[i] for i in results[0]]
    context = " ".join(relevant)

    response = qa(question=query, context=context)

    return response["answer"]


print(ask_question("Most popular language?"))
print(ask_question("World the Highest mountain?"))
