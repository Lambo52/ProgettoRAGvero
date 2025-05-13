from RAGsystem.embeddings import client

def AdjustQuery(query):    
    
    system_prompt = """Sei un assistente specializzato nel rendere una query migliore per la ricerca sui documenti, ti verrà dato in input una query e dovrai riscriverla per renderla più efficace basandoti esclusivamente sul contesto fornito. dovrai rispondere in questo modo: <query riscritta da te>. non aggiungere altro al messaggio"""
    
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ],
        model="llama3-8b-8192", #siamo sull'8b
        temperature=0.1,
        max_tokens=1024
    )
    
    print("query riscritta: ", response.choices[0].message.content)
    return response.choices[0].message.content



