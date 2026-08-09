from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


def create_retriever():

    # Load company document
    loader = TextLoader(
        "documents/taskinfo.txt",
        encoding="utf-8"
    )

    docs = loader.load()

    # Split document into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(docs)

    # Local Hugging Face embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Create Chroma vector database
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    return vector_db.as_retriever(
        search_kwargs={"k": 3}
    )


retriever = create_retriever()


def retrieve_documents(state):

    question = state["question"]

    results = retriever.invoke(question)

    documents = [
        doc.page_content
        for doc in results
    ]

    return {
        "documents": documents
    }