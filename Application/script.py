from RAGsystem.embeddings import *
from RAGsystem.agentAI import *
from GoogleAPI.gmail import *
from RAGsystem.writemails import *
from RAGsystem.Search import query
from RAGsystem.QueryAdjustment import AdjustQuery
from setLocalEmails import return_mails
from RAGsystem.IterativeK import iterativek
import time

def start(domanda,topk = 5,adjustquery = True, mode2 = False):

    emails,emaileliminate,mailtotali = return_mails()

    vectorstore = generate_embeddings(emails,emaileliminate,mailtotali)
    
    queryadjusted = ""

    if adjustquery:
        queryadjusted = AdjustQuery(domanda)
    else:
        queryadjusted = domanda
    
    if mode2:
        results = iterativek(domanda,vectorstore,queryadjusted)#qua devo prendere i primi 5, opi se sono rilevanti ne prendo altri 5 e così via, chiamo da qua la funzione query
    else:
        results = query(domanda,vectorstore,queryadjusted,topk)

    context = "\n\n".join([f"Mail {i+1}: {doc.page_content}\n{doc.metadata}" for i, doc in enumerate(results)])
    
    risposta = query_with_llm(context, domanda)

    generateEmail(risposta)


queryiniziale = "ci sono visite mediche in programma per i dipendenti?"

start(queryiniziale,topk=5,adjustquery=True,mode2=False)

# RICORDARSI DI CANCELLARE FAISS_INDEX E DB SE SI VUOLE RESTARTARE, SE NO OBV CARICA LE MAIL SULLO STESSO VDB

#TODO: controllare metadati dato che è andato tutto al primo tentativo

#TODO: implementare HNSW con FAISS per poi fare ricerche di k in k (impossibile farlo con langchain, quindi farlo con flatl2 e bella)

#TODO: migliorare la gestione delle mail, adesso vengono scaricate tutte le mail ogni volta ma non so come risolvere cristoddio




