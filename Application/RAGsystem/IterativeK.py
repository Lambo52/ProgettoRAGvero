from RAGsystem.Search import query
from RAGsystem.embeddings import client


def contextevaluationllm(context, query):
        
    system_prompt = """Sei un assistente specializzato nell'analisi di email. 
    Devi dire se ci sono documenti rilevanti per la domanda posta, non rispondere alla domanda, il tuo unico scopo è scrivere se ci sono documenti rilevanti o no e se ci sono dire quali documenti.rispondi con "no" o con i documenti rilevanti, se ad esempio i documenti rilevanti sono il primo e il terzo dovrai scrivere "1,3" e basta."""
    
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Contesto:\n{context}\n\nDomanda: {query}"}
        ],
        model="llama3-8b-8192", #sempre 8b
        temperature=0.1,
        max_tokens=1024
    )
    
    # risultati rag
    print("\n--- DOMANDA POSTA ---")
    print(query)
    print("\n--- RISPOSTA GENERATA --- modello " + str(response.model))
    print(response.choices[0].message.content)
    
    return response.choices[0].message.content



def iterativek(domanda,vectorstore,queryadjusted):
    k = 5
    contexttotale = ""

    context = query(domanda, vectorstore,k)

    while contextevaluationllm(context,queryadjusted) != "no" or contextevaluationllm(context,queryadjusted) != "No":
        k += 5
        context = query(context, vectorstore,k)
        context = context[4:]

    
    return None, 

iterativek("visite mediche dipendenti",lesgoooooooooooooooo,"visite mediche dipendenti")