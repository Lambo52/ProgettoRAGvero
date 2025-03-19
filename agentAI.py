from embeddings import *


def query(query, vectorstore,queryaggiustata,k):

    
    """vectorstore = FAISS.load_local(
        "faiss_index",
        embedding,
        allow_dangerous_deserialization=True
    )"""
    
    # similarity search
    results = vectorstore.similarity_search(queryaggiustata, k)

    context = "\n\n".join([f"Mail {i+1}: {doc.page_content}" for i, doc in enumerate(results)])

    print("\n--- MAIL DI RIFERIMENTO ---")
    for i, doc in enumerate(results):
        print(f"Mail {i+1}:\n{doc.page_content}")
    
    return context,query

def query_with_llm(context, query):
    
    
    
    
    system_prompt = """Sei un assistente specializzato nell'analisi di email. 
    Rispondi alla domanda basandoti esclusivamente sul contesto fornito."""
    
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Contesto:\n{context}\n\nDomanda: {query}"}
        ],
        model="llama3-8b-8192", #siamo sull'8b
        temperature=0.5,
        max_tokens=1024
    )
    
    # risultati rag
    print("\n--- DOMANDA POSTA ---")
    print(query)
    print("\n--- RISPOSTA GENERATA --- modello " + str(response.model))
    print(response.choices[0].message.content)
    
    return response.choices[0].message.content


