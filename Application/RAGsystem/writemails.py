from RAGsystem.embeddings import client


def generateEmail(rispostallm):

    risposta = input("Vuoi inviare una mail di risposta?")
    
    
    
    # Formattazione prompt per Groq
    system_prompt = """Sei un assistente specializzato nella scrittura di email aziendali, in input riceverai un riassunto delle mail e ti verrà chiesto di scrivere una nuova email in risposta, scrivi in italiano; il nome da inserire alla fine della mail è "Lambo". Se l'utente non vuole inviare la mail o se scrive "no", scrivi "ok"."""
    
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Contesto:\n{rispostallm}\n\nDomanda: {risposta}"}
        ],
        model="llama3-8b-8192", #siamo sull'8b
        temperature=0.5,
        max_tokens=1024
    )

    print("\n--- RISPOSTA GENERATA PER SCRITTURA MAIL --- modello " + str(response.model))
    print(response.choices[0].message.content)


