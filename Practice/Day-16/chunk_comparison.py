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

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

llm = ChatGoogleGenerativeAI(
    model="models/gemini-3.5-flash",
    temperature=0
)

question = "How many paid leaves are employees allowed?"

for size in [200, 400, 800]:
    print("\n" + "=" * 60)
    print(f"Chunk Size: {size}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=size,
        chunk_overlap=50
    )

    docs = splitter.split_documents(documents)

    db = FAISS.from_documents(docs, embedding)

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=db.as_retriever()
    )

    response = qa.invoke({"query": question})

    print("Chunks:", len(docs))
    print("Answer:", response["result"])