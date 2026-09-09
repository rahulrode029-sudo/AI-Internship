from dotenv import load_dotenv

load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA

print("=" * 60)
print("      COMPANY DOCUMENT AI ASSISTANT (Gemini)")
print("=" * 60)

# Load document
loader = TextLoader("data/company_docs.txt", encoding="utf-8")
documents = loader.load()

# Split document into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=50
)

docs = splitter.split_documents(documents)

# Hugging Face embeddings
embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Create Chroma database
db = Chroma.from_documents(
    docs,
    embedding,
    persist_directory="chroma_db"
)

retriever = db.as_retriever(search_kwargs={"k": 3})

# Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="models/gemini-3.5-flash",
    temperature=0
)

# RAG pipeline
qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever
)

while True:
    question = input("\nAsk your question (type exit to quit): ")

    if question.lower() == "exit":
        print("\nThank you for using the AI Assistant.")
        break

    result = qa.invoke({"query": question})

    print("\nAI Answer:\n")
    print(result["result"])