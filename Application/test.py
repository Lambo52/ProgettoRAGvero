from setLocalEmails import return_mails
from RAGsystem.embeddings import *


emails,emaileliminate,mailtotali = return_mails()

vectorstore = generate_embeddings(emails,emaileliminate,mailtotali)

results = vectorstore.similarity_search("riunioni straordinarie per i dipendenti",3)

for i, doc in enumerate(results):
    print(f"Mail {i+1}:\n{doc.page_content}\n{doc.metadata}")

results = vectorstore.similarity_search("riunioni straordinarie per i dipendenti",6)

for i, doc in enumerate(results):
    print(f"Mail {i+1}:\n{doc.page_content}\n{doc.metadata}")

results = vectorstore.similarity_search("riunioni straordinarie per i dipendenti",9)

for i, doc in enumerate(results):
    print(f"Mail {i+1}:\n{doc.page_content}\n{doc.metadata}")

results = vectorstore.similarity_search("riunioni straordinarie per i dipendenti",12)

for i, doc in enumerate(results):
    print(f"Mail {i+1}:\n{doc.page_content}\n{doc.metadata}")


results = vectorstore.similarity_search("riunioni straordinarie per i dipendenti",15)

for i, doc in enumerate(results):
    print(f"Mail {i+1}:\n{doc.page_content}\n{doc.metadata}")
