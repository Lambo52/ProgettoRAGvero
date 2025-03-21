import os
from groq import Groq
import numpy as np
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
#from mails import emails
from dotenv import load_dotenv
load_dotenv()

# modello da 1 giga e passa ma 512 token di massimo
#embedding = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large")
embedding = OpenAIEmbeddings(model="text-embedding-3-small",openai_api_key=os.environ.get("OPENAI_API_KEY"))

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def generate_embeddings(emails,emaileliminate,emailtotali):

    no_splitter = RecursiveCharacterTextSplitter(
    chunk_size=10000,  # se arriva una mail più lunga di 10000 caratteri non ha senso
    chunk_overlap=0
    )

    base_documents = [Document(page_content=email) for email in emails]

    split_docs = no_splitter.split_documents(base_documents)

    if os.path.exists("faiss_index"):
        # carichiamo indice esistente che tanto so per certo che esiste
        vectorstore = FAISS.load_local("faiss_index", embeddings=embedding,allow_dangerous_deserialization=True)
        # aggiungo e tolgo mail se necessario
        if emails:
            print("ci sono nuove emails, aggiorno l'indice")
            vectorstore.add_documents(split_docs)
        if emaileliminate:
            print("ci sono emails eliminate, riscrittura dell'indice in corso")
            base_documents = [Document(page_content=email) for email in emailtotali]
            split_docs = no_splitter.split_documents(base_documents)
            vectorstore = FAISS.from_documents(documents=split_docs, embedding=embedding)
    else:
        # lo creo se non esiste
        print("creazione indice")
        vectorstore = FAISS.from_documents(documents=split_docs, embedding=embedding)
    
    vectorstore.save_local("faiss_index")
    #print(f"Numero mails: {len(split_docs)}")
    return vectorstore






