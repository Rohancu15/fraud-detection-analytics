from services.chroma_client import add_documents, query_documents

docs = [
    "Multiple transactions in short time indicate fraud",
    "Transactions from different countries are suspicious",
    "Unusual login attempts may indicate account breach"
]

# Add data
add_documents(docs)

# Query
query = "User made transactions from different locations"

results = query_documents(query)

print("Relevant Documents:")
for r in results:
    print(r)