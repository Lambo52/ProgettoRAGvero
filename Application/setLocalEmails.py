from Database.dbfunctions import DBManager
from GoogleAPI.gmail import *
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

def return_mails():
    service = create_service()

    # if not new_emails(service):
    #     return []

    messages = get_email_messages(service, max_results=100)
    mails = []
    mailstot = []

    #conn = initialize_db() #DATABASE
    db_manager = DBManager() #DATABASE, CREA TABELLE SE NON ESISTONO

    stored_date = db_manager.get_stored_date() #DATABASE
    
    # variabile inutile ma non toglierla per sicurezza
    latest_relevant_date = stored_date

    # id esistenti nel nostro vdb
    stored_ids = db_manager.load_stored_ids() #DATABASE

    
    current_ids = []

    for msg in reversed(messages):
        details = get_email_message_details(service, msg['id'])
        current_ids.append(msg['id'])
        
        # finalmente data va bene lasciala così
        mail_date = parsedate_to_datetime(details['date'])
        if mail_date.tzinfo is None:
            mail_date = mail_date.replace(tzinfo=timezone.utc)
        
        
#        if stored_date is None or mail_date > stored_date:
#            mails.append(f"Oggetto: {details['subject']} Corpo: {details['body']}")
#        mailstot.append(f"Oggetto: {details['subject']} Corpo: {details['body']}")

            
        #NUOVO QUA, CAMBIATO TUTTO, CONTROLLARE
        metadata = {
            'subject': details['subject'],
            'sender': details['sender']
        }
        vettorelocale = (details['body'],metadata)

        # storing di mail aggiornate e totali in caso di eliminazione
        if stored_date is None or mail_date > stored_date:
            mails.append(vettorelocale)
        mailstot.append(vettorelocale)
        #così mail è una lista di liste, ogni lista contiene [metadata,body], metadata contiene [subject,sender]


            
        # funzione inutile ma ho paura a toglierla (no in realtà è utile, latest_relevannt_date serve perché dobbiamo fare il confronto per ogni mail, inoltre se non esistono mail ci serve per non salvare niente)
        if latest_relevant_date is None or mail_date > latest_relevant_date:
            latest_relevant_date = mail_date

    # controllo mail eliminate
    
    deleted_ids = [mail_id for mail_id in stored_ids if mail_id not in current_ids]
    
        

    
    db_manager.save_ids(current_ids) #DATABASE

    
    if latest_relevant_date is not None and (stored_date is None or latest_relevant_date > stored_date):
        db_manager.setdate(latest_relevant_date) #DATABASE
    
    db_manager.close() #DATABASE

    #close_database(conn)

    return mails,deleted_ids,mailstot