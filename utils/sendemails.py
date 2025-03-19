import os
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from utils.GoogleColdStart import create_service

from embeddings import *


def send_email(service, to, subject, body, body_type='plain', attachment_paths=None):
    message = MIMEMultipart()
    message['to'] = to
    message['subject'] = subject

    if body_type.lower() not in ['plain', 'html']:
        raise ValueError("body_type must be either 'plain' o 'html'")

    message.attach(MIMEText(body, body_type.lower()))

    """if attachment_paths:
        for attachment_path in attachment_paths:
            if os.path.exists(attachment_path):
                filename = os.path.basename(attachment_path)
                with open(attachment_path, 'rb') as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())

                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename= {filename}")
                message.attach(part)
            else:
                raise FileNotFoundError(f"File not found - {attachment_path}")"""

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

    sent_message = service.users().messages().send(
        userId = 'me',
        body = {'raw': raw_message}).execute()
    
    return sent_message





def send_email_llm():
    
    
    
    # Formattazione prompt per Groq
    system_prompt = """Sei un assistente specializzato nel fornire email aziendali, la risposta deve essere una mail aziendale, il formato deve essere <oggetto> <testo dell'oggetto> <body> <testo del body>, esempio: <oggetto> Promozione sui tagliaerba <body> Buongiorno Si informa che da domani 14/03/2025 i tagliaerba costeranno la metà perché l'azienda erbacorta chiude, vi invitiamo a non perdere questa occasione.
    altro esempio: <oggetto> Visite mediche dipendenti <body> Buonasera, si informa che la prossima settimana ci saranno visite mediche per tutti i dipendenti in quanto teniamo alla salute dei nostri lavoratori, contattare l'ufficio per prendere l'appuntamento.
    """
    
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Scrivimi una mail aziendale, inventa un oggetto e un corpo della mail, puoi inserire nomi e date ma inventale"}
        ],
        model="qwen-2.5-32b", #qwen per generazione mail
        temperature=0.5,
        max_tokens=1024
    )
    
    # Stampa risultati
    print("\n--- RISPOSTA GENERATA --- modello " + str(response.model))
    print(response.choices[0].message.content)
    return response.choices[0].message.content


for i in range(0, 90):

    mail_llm = send_email_llm()

    oggetto = mail_llm.split("<oggetto>")[1].split("<body>")[0]
    body = mail_llm.split("<body>")[1]

    print(oggetto)
    print(body)

    service = create_service()

    to_address = 'lambo.fra01@gmail.com'
    email_subject = oggetto
    email_body = body

    response_email_sent = send_email(service, to_address, email_subject, email_body)

    print(response_email_sent)


