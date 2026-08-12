from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


def create_retriever():

    loader = TextLoader(
        "documents/taskinfo.txt",
        encoding="utf-8"
    )

    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    return vector_db.as_retriever(
        search_kwargs={"k": 3}
    )


retriever = create_retriever()