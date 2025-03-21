from GoogleAPI.GoogleColdStart import create_service
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64
import os
from email.mime.base import MIMEBase
from email import encoders



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
