from utils.GoogleColdStart import create_service
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64
import os
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import json


#print(dir(service))

# LEGGIAMO MAIL


def _extract_body(payload):
    body = '(body not available)'
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'multipart/alternative':
                for subpart in part['parts']:
                    if subpart['mimeType'] == 'text/plain' and 'data' in subpart['body']:
                        body = base64.urlsafe_b64decode(subpart['body']['data']).decode('utf-8')
                break
            elif part['mimeType'] == 'text/plain' and 'data' in part['body']:
                body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                break
    elif 'body' in payload and 'data' in payload['body']:
        body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
    return body


def get_email_messages(service, user_id='me', label_ids=None, folder_name='INBOX', max_results=5):
    folder_label_id = None
    next_page_token = None
    messages = []

    
    if folder_name:
        folders = service.users().labels().list(userId=user_id).execute().get('labels', [])
        for label in folders:
            if label['name'].lower() == folder_name.lower():
                folder_label_id = label['id']
                break
        if not folder_label_id:
            raise ValueError(f"Folder '{folder_name}' not found.")

    #ciclo per ottenere tutti i messaggi
    while True:
        results = service.users().messages().list(
            userId=user_id,
            labelIds=label_ids if label_ids else [folder_label_id],
            maxResults=min(max_results - len(messages), 500) if max_results else 500,
            pageToken=next_page_token
        ).execute()

        messages_batch = results.get('messages', [])
        if messages_batch:
            messages.extend(messages_batch)

        next_page_token = results.get('nextPageToken')
        
        
        if not next_page_token or (max_results and len(messages) >= max_results):
            break

    return messages[:max_results] if max_results else messages


def get_email_message_details(service, msg_id):
    
    message = service.users().messages().get(
        userId='me',
        id=msg_id,
        format='full'
    ).execute()
    
    
    subject = next(
        header['value'] for header in message['payload'].get('headers', [])
        if header['name'].lower() == 'subject'
    )
    sender = next(
        header['value'] for header in message['payload'].get('headers', [])
        if header['name'].lower() == 'from'
    )
    recipients = next(
        header['value'] for header in message['payload'].get('headers', [])
        if header['name'].lower() == 'to'
    )
    
    
    snippet = message.get('snippet', '')
    body = _extract_body(message['payload'])
    
    
    date = next(
        header['value'] for header in message['payload'].get('headers', [])
        if header['name'].lower() == 'date'
    )
    
    
    has_attachments = any(
        part.get('filename')
        for part in message['payload'].get('parts', [])
        if part.get('filename')
    )
    
    
    starred = 'STARRED' in message.get('labelIds', [])
    
    
    label = ', '.join(message.get('labelIds', []))

    return {
        'subject': subject,
        'sender': sender,
        'recipients': recipients,
        'snippet': snippet,
        'body': body,
        'date': date,
        'has_attachments': has_attachments,
        'star': starred,
        'label': label,
    }








def setdate(date): #NON TOCCARE NIENTE QUI
    if isinstance(date, str):
        date = parsedate_to_datetime(date)
    if date.tzinfo is None:
        date = date.replace(tzinfo=timezone.utc)
    with open('last_date.txt', 'w') as f:
        f.write(date.isoformat())

def get_stored_date(): #NON TOCCARE NIENTE QUI
    if not os.path.exists('last_date.txt'):
        return None
    try:
        with open('last_date.txt', 'r') as f:
            return datetime.fromisoformat(f.read().strip())
    except Exception as e:
        print(f"Errore lettura data salvata: {e}")
        return None
    
"""def new_emails(service): 
    message = get_email_messages(service, max_results=1)
    stored_date = get_stored_date()
    details = get_email_message_details(service, message[0]['id'])
    mail_date = parsedate_to_datetime(details['date'])
    if mail_date.tzinfo is None:
        mail_date = mail_date.replace(tzinfo=timezone.utc)
    
    if stored_date is None or mail_date > stored_date:
        return False
    return True
"""    



#id mail per eliminazione mail
def load_stored_ids(file_path="mail_ids.json"):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return []

def save_ids(ids, file_path="mail_ids.json"):
    with open(file_path, "w") as f:
        json.dump(ids, f)

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

