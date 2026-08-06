from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA

loader = TextLoader("data/company_docs.txt", encoding="utf-8")
documents = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
docs = splitter.split_documents(documents)

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.from_documents(docs, embedding)

llm = ChatGoogleGenerativeAI(
    model="models/gemini-3.5-flash",
    temperature=0
)

qa = RetrievalQA.from_chain_type(llm=llm, retriever=db.as_retriever())

while True:
    q = input("\nQuestion: ")

    if q.lower() == "exit":
        break

    result = qa.invoke({"query": q})
    print("\n", result["result"])