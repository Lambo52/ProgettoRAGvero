from RAGsystem.Search import *
from RAGsystem.embeddings import client, embedding
#from langchain_community.vectorstores import FAISS
from RAGsystem.embeddings import *

def contextevaluationllm(context, query, aumento):
        
    system_prompt = f"""Sei un assistente specializzato nell'analisi di email. 
    Devi dire per ogni mail se risponde o no alla domanda posta, il tuo unico scopo è scrivere se ci sono mail rilevanti o no.
    rispondi con "0" se la mail non è rilevante, con "1" se lo è, non aver paura di dire che nessun documento è rilevante, se ad esempio i documenti rilevanti sono il primo e il terzo e ci sono 3 documenti totali, dovrai scrivere "1 0 1" e basta. Mi raccomando di non aggiungere altro al messaggio, non scrivere "le mail rilevanti sono la 1 e la 3" o cose simili, ma solo "1 0 1". in questo caso ci sono {aumento} documenti, quindi dovrai scrivere {aumento} numeri."""
    
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Contesto:\n{context}\n\nDomanda: {query}"}
        ],
        model="qwen-qwq-32b",
        temperature=0.1,
        max_tokens=2048
    )
    
    # risultati rag
    #print("\n--- DOMANDA POSTA ---")
    #print(query)
    #print("\n--- RISPOSTA GENERATA --- modello " + str(response.model))
    #print(response.choices[0].message.content)
    
    return response.choices[0].message.content



def iterativek(domanda,vectorstore,queryadjusted,k):
    aumento = k
    contexttotale = []

    results = query(vectorstore,queryadjusted,k,False)
    contextlocale = "\n\n".join([f"Mail {i+1}: {doc.page_content}\n{doc.metadata}" for i, doc in enumerate(results)])
    contextbackup = results
    rispostallm = contextevaluationllm(contextlocale, domanda, aumento)
    print(rispostallm)
    rispostaaggiustata = rispostallm.split("</think>")[1].strip()

    vettorebitmap = [int(i) for i in rispostaaggiustata.split()]
    print(vettorebitmap)

    for i,elemento in enumerate(vettorebitmap):
        if elemento == 1:
            contexttotale.append(results[i])
    #print(contexttotale)

    while 1 in vettorebitmap:
        k+=aumento
        if k > 20:
            break
        
        results = query(vectorstore,queryadjusted,k,False)
        results = results[-aumento:]
        contextlocale = "\n\n".join([f"Mail {i+1}: {doc.page_content}\n{doc.metadata}" for i, doc in enumerate(results)])
        rispostallm = contextevaluationllm(contextlocale, domanda,aumento)
        rispostaaggiustata = rispostallm.split("</think>")[1].strip()
        print(rispostallm)
        vettorebitmap = [int(i) for i in rispostaaggiustata.split()]
        print(vettorebitmap)
        for i,elemento in enumerate(vettorebitmap):
            if elemento == 1:
                contexttotale.append(results[i])
    
    print("\n--- MAIL DI RIFERIMENTO PER ITERATIVE ---")
    for i, doc in enumerate(contexttotale):
        print(f"\n\nMail {i+1}:\n{doc.page_content}\n{doc.metadata}")
    
    if len(contexttotale) == 0:
        contexttotale = contextbackup
    
    return contexttotale



#vectorstore = vectorstore = FAISS.load_local("faiss_index", embeddings=embedding,allow_dangerous_deserialization=True)
#iterativek("ci sono visite mediche in programma per i dipendenti?",vectorstore,"Visite mediche dipendenti")