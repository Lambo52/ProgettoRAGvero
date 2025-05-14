from RAGsystem.embeddings import client



def query_with_llm(context, query):
        
    system_prompt = """Sei un assistente specializzato nell'analisi di email. 
    Rispondi alla domanda basandoti esclusivamente sul contesto fornito."""
    
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Contesto:\n{context}\n\nDomanda: {query}"}
        ],
        model="qwen-qwq-32b",
        temperature=0.5,
        max_tokens=2048
    )
    
    # risultati rag
    print("\n--- DOMANDA POSTA ---")
    print(query)
    print("\n--- RISPOSTA GENERATA --- modello " + str(response.model))
    print(response.choices[0].message.content.split("</think>")[1].strip())
    
    return response.choices[0].message.content.split("</think>")[1].strip()


