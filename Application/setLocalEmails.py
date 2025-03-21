from Database.dbfunctions import *
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

    stored_date = get_stored_date()
    
    # variabile inutile ma non toglierla per sicurezza
    latest_relevant_date = stored_date

    # id esistenti nel nostro vdb
    stored_ids = load_stored_ids()

    
    current_ids = []

    for msg in reversed(messages):
        details = get_email_message_details(service, msg['id'])
        current_ids.append(msg['id'])
        
        # finalmente data va bene lasciala così
        mail_date = parsedate_to_datetime(details['date'])
        if mail_date.tzinfo is None:
            mail_date = mail_date.replace(tzinfo=timezone.utc)

        # storing di mail aggiornate e totali in caso di eliminazione
        if stored_date is None or mail_date > stored_date:
            mails.append(f"Oggetto: {details['subject']} Corpo: {details['body']}")
        mailstot.append(f"Oggetto: {details['subject']} Corpo: {details['body']}")
            
        # funzione inutile ma ho paura a toglierla
        if latest_relevant_date is None or mail_date > latest_relevant_date:
            latest_relevant_date = mail_date

    # controllo mail eliminate
    
    deleted_ids = [mail_id for mail_id in stored_ids if mail_id not in current_ids]
    
        

    
    save_ids(current_ids)

    
    if latest_relevant_date is not None and (stored_date is None or latest_relevant_date > stored_date):
        setdate(latest_relevant_date)

    return mails,deleted_ids,mailstot