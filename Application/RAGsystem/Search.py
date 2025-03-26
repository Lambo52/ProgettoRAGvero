

def query(query, vectorstore,queryaggiustata,k):

    
    """vectorstore = FAISS.load_local(
        "faiss_index",
        embedding,
        allow_dangerous_deserialization=True
    )"""
    
    # similarity search
    results = vectorstore.similarity_search(queryaggiustata, k)

    #riga sacra, ma ci serve dopo
    #context = "\n\n".join([f"Mail {i+1}: {doc.page_content}\n{doc.metadata}" for i, doc in enumerate(results)])

    print("\n--- MAIL DI RIFERIMENTO ---")
    for i, doc in enumerate(results):
        print(f"Mail {i+1}:\n{doc.page_content}\n{doc.metadata}")
    
    return results