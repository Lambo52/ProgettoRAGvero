from embeddings import *
from agentAI import *
from gmail import *
from writemails import *
from QueryAdjustment import AdjustQuery
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

#TODO: migliorare la gestione delle mail, adesso vengono scaricate tutte le mail ogni volta ma non so come risolvere cristoddio

#TODO: mettere mail ids e last_date su un db madonna




