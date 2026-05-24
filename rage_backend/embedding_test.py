from sentence_transformers import SentenceTransformer
model=SentenceTransformer("all-MiniLM-L6-v2")

sentences=[
    "JWT authentication",
    "Token verification",
    "Banana Milkshake"
]
embeddings=model.encode(sentences)

for sentence,embedding in zip(sentences,embeddings):
    print(f"\nSentence: {sentence}")
    print(f"Vector length: {len(embedding)}")
    print(embedding[:5]) #here we are just retreiveing the first 5 chunks off 384 i.e vector length, all 384 are like dimesnions and are equally important 