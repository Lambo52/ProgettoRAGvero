from RAGsystem.embeddings import *
from RAGsystem.agentAI import *
from GoogleAPI.gmail import *
from RAGsystem.writemails import *
from RAGsystem.Search import query
from RAGsystem.QueryAdjustment import AdjustQuery
from setLocalEmails import return_mails
from RAGsystem.IterativeK import iterativek
import time

def start(domanda,topk = 5,adjustquery = True, llmevaluation = False, answer = True):

    emails,emaileliminate,mailtotali = return_mails()

    vectorstore = generate_embeddings(emails,emaileliminate,mailtotali)
    
    queryadjusted = ""

    if adjustquery:
        queryadjusted = AdjustQuery(domanda)
    else:
        queryadjusted = domanda
    
    if llmevaluation:
        #pass
        results = iterativek(domanda,vectorstore,queryadjusted,topk)#qua devo prendere i primi 5, se sono rilevanti ne prendo altri 5 e così via, chiamo da qua la funzione query, e serve la domanda per la valutazione
    else:
        results = query(vectorstore,queryadjusted,topk)

    context = "\n\n".join([f"Mail {i+1}: {doc.page_content}\n{doc.metadata}" for i, doc in enumerate(results)])
    
    
    risposta = query_with_llm(context, domanda)

    if answer:
        generateEmail(risposta)
    else:
        pass

evaluation = ["sono presenti mail della tavola rotonda sull'intelligenza artificiale?",#iterative ok/ok, topk ok
             "ci sono mail che parlano di blockchain o di corsi sulla blockchain?",#iterative ok/ok, topk ok
             "c'è qualche convegno sulla sicurezza informatica in programma?", #iterative sbagliato/sbagliato, topk ok
             "è presente qualche adeguamento al gdpr?",#iterative ok/ok, topk ok
             "cosa comporta la chiusura dell'anno fiscale?",#iterative ok/sbagliato, topk ok 
             "c'è qualche mail riguardante l'ufficio personale?",#iterative ok/ok, topk ok
             "sono previste visite mediche aziendali?",#iterative ok/ok, topk ok
             "ci sono novità per quanto riguarda il contratto di affitto?",#iterative ok/ok, topk ok
             "è stato aperto un ticket per un problema?",#iterative sbagliato/ok, topk ok
             "c'è qualche corso di preparazione per excel?",#iterative ok, topk ok
             "avrei bisogno di un tagliaerba, ci sono offerte?",#iterative ok, topk ok
             "come procede il progetto alpha?",#iterative ok, topk ok
             "ci sono mail urgenti?",#iterative ok, topk più o meno ok
             "com'è il clima aziendale?",#iterative sbagliato, topk ok
             "ci sono mail riguardanti l'ambiente di lavoro in azienda?"]#iterative ok, topk ok

#queryiniziale = "sono presenti mail della tavola rotonda sull'intelligenza artificiale?"
#queryiniziale = "ci sono mail che parlano di blockchain o di corsi sulla blockchain?"
#queryiniziale = "c'è qualche convegno sulla sicurezza informatica in programma?"
#queryiniziale = "è presente qualche adeguamento al gdpr?"
#queryiniziale = "cosa comporta la chiusura dell'anno fiscale?"
#queryiniziale = "c'è qualche mail riguardante l'ufficio personale?"
#queryiniziale = "sono previste visite mediche aziendali?"
#queryiniziale = "ci sono novità per quanto riguarda il contratto di affitto?"
#queryiniziale = "è stato aperto un ticket per un problema?"
#queryiniziale = "c'è qualche corso di preparazione per excel?"
#queryiniziale = "avrei bisogno di un tagliaerba, ci sono offerte?"
#queryiniziale = "come procede il progetto alpha?"
queryiniziale = "ci sono mail urgenti?"
#queryiniziale = "com'è il clima aziendale?"
#queryiniziale = "ci sono mail riguardanti l'ambiente di lavoro in azienda?"

#for queryiniziale in evaluation:

start(queryiniziale,topk=3,adjustquery=True,llmevaluation=True, answer=False)
#start(queryiniziale,topk=5,adjustquery=True,llmevaluation=False)
#start(queryiniziale,topk=5,adjustquery=False,llmevaluation=False)
#start(queryiniziale,topk=5,adjustquery=False,llmevaluation=True)

# RICORDARSI DI CANCELLARE FAISS_INDEX E DB SE SI VUOLE RESTARTARE, SE NO OBV CARICA LE MAIL SULLO STESSO VDB

#TODO: controllare meglio il file embeddings, se ci sono mail eliminate e nuove deve essere un caso, fare i casi 1 per 1

#TODO: controllare metadati dato che è andato tutto al primo tentativo

#TODO: migliorare la gestione delle mail, adesso vengono scaricate tutte le mail ogni volta ma non so come risolvere cristoddio




