import os

from dotenv import load_dotenv

load_dotenv()

from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI
)

from langchain_community.document_loaders import TextLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import Chroma

from langchain.chains import RetrievalQA

from langchain_huggingface import HuggingFaceEmbeddings


loader = TextLoader("data/company_docs.txt")

documents = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

docs = splitter.split_documents(documents)


#embedding = GoogleGenerativeAIEmbeddings(
#1    model="models/embedding-001"
#)

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma.from_documents(
    docs,
    embedding,
    persist_directory="chroma_db"
)

retriever = db.as_retriever(search_kwargs={"k":3})

llm = ChatGoogleGenerativeAI(
    model="models/gemini-3.5-flash",
    temperature=0
)

qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever
)

print("="*60)
print("COMPANY DOCUMENT AI")
print("="*60)

while True:

    question = input("\nAsk Question : ")

    if question.lower()=="exit":
        break

    answer = qa.invoke(question)

    print("\nAnswer\n")
    print(answer["result"])