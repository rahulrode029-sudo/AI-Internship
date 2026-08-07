import os

from dotenv import load_dotenv

from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()


# -----------------------------
# Embedding Model
# -----------------------------

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# -----------------------------
# Gemini LLM
# -----------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    temperature=0
)


DB_DIR = "chroma_db"


# -----------------------------
# Process PDF
# -----------------------------

def process_pdf(pdf_path):

    loader = PyPDFLoader(pdf_path)

    documents = loader.load()


    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )


    chunks = splitter.split_documents(documents)


    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embedding,
        persist_directory=DB_DIR
    )


    return len(chunks)



# -----------------------------
# Ask Question
# -----------------------------

def ask_question(question):


    vectordb = Chroma(
        persist_directory=DB_DIR,
        embedding_function=embedding
    )


    results = vectordb.similarity_search(
        question,
        k=4
    )


    context = "\n\n".join(
        doc.page_content
        for doc in results
    )


    prompt = f"""

Answer only using the given context.

Context:
{context}


Question:
{question}

"""


    response = llm.invoke(prompt)


    return response.content
