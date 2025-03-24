from RAGsystem.embeddings import *
from RAGsystem.agentAI import *
from GoogleAPI.gmail import *
from RAGsystem.writemails import *
from RAGsystem.QueryAdjustment import AdjustQuery
from setLocalEmails import return_mails
import time

def start(domanda,topk = 5,adjustquery = True):

    emails,emaileliminate,mailtotali = return_mails()

    vectorstore = generate_embeddings(emails,emaileliminate,mailtotali)
    
    queryadjusted = ""
    if adjustquery:
        queryadjusted = AdjustQuery(domanda)
    else:
        queryadjusted = domanda
    
    context, query_result = query(domanda,vectorstore,queryadjusted,topk)

    risposta = query_with_llm(context, query_result)

    generateEmail(risposta)


queryiniziale = "ci sono visite mediche in programma per i dipendenti?"

start(queryiniziale,5,True)

# RICORDARSI DI CANCELLARE FAISS_INDEX E DB SE SI VUOLE RESTARTARE, SE NO OBV CARICA LE MAIL SULLO STESSO VDB

#TODO: migliorare la gestione delle mail, adesso vengono scaricate tutte le mail ogni volta ma non so come risolvere cristoddio

#TODO: controllare metadati dato che è andato tutto al primo tentativo

#TODO: implementare HNSW con FAISS per poi fare ricerche di k in k (impossibile farlo con langchain, quindi farlo con flatl2 e bella)






