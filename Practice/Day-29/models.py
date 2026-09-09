from pydantic import BaseModel


class QuestionRequest(BaseModel):
    question: str


class QuestionResponse(BaseModel):
    question: str
    answer: str
    sources: list[str]


class HealthResponse(BaseModel):
    status: str
    version: str


class DocumentInfo(BaseModel):
    filename: str
    file_type: str
    size_bytes: int
    content: str


class DocumentsResponse(BaseModel):
    total_documents: int
    documents: list[DocumentInfo]
    total_chunks: int