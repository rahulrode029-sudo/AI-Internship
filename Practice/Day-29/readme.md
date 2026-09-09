# AI Document Question Answering System

## Project Overview

The AI Document Question Answering System is a FastAPI-based application that allows users to upload documents and ask questions based on the uploaded document content.

The application supports PDF, DOCX, and TXT files. Uploaded documents are processed, cleaned, divided into smaller chunks, and indexed using TF-IDF. When a user asks a question, the system retrieves the most relevant document chunks and generates an answer using the configured AI service.

A document viewing feature has also been added so users can see the actual extracted content of their uploaded documents.

---

## Objectives

The main objectives of this project are:

- Upload PDF, DOCX, and TXT documents.
- Extract text from uploaded documents.
- Clean and process document text.
- Divide documents into smaller chunks.
- Retrieve relevant information from documents.
- Allow users to ask questions about uploaded documents.
- Allow users to view uploaded document content.
- Provide REST APIs using FastAPI.
- Handle invalid and empty files.
- Test the complete application using Pytest.

---

## Key Features

### 1. Document Upload

Users can upload:

- PDF files
- DOCX files
- TXT files

Uploaded files are stored in the `documents/` directory.

### 2. Document Content Viewing

The project provides:

```text
GET /documents

This endpoint allows users to view uploaded documents and their extracted content.

The response contains:

Filename
File type
File size
Extracted document content
Number of uploaded documents
Number of document chunks

Example response:

{
  "total_documents": 1,
  "documents": [
    {
      "filename": "example.txt",
      "file_type": ".txt",
      "size_bytes": 100,
      "content": "This is the content of my uploaded document."
    }
  ],
  "total_chunks": 1
}
3. Document Processing

The application extracts text from:

TXT using Python file handling
PDF using PyPDF
DOCX using python-docx
4. Text Cleaning

The extracted text is cleaned by removing unnecessary whitespace and empty lines.

5. Text Chunking

Large documents are divided into smaller chunks.

Each chunk contains:

Text
Metadata
Chunk index

Example:

DocumentChunk(
    text="Document content...",
    metadata={
        "chunk_index": 0
    }
)
6. TF-IDF Retrieval

The application uses TF-IDF vectorization to convert document chunks into numerical vectors.

7. Cosine Similarity

Cosine similarity is used to compare the user's question with document chunks and identify the most relevant information.

8. Question Answering

Users can ask questions using:

POST /ask

The system retrieves relevant document chunks and sends the information to the AI service to generate an answer.

9. Automated Testing

The project uses Pytest for automated testing.

Current result:

21 tests passed
Problem Statement

Searching through large documents manually can be time-consuming.

Users may need to find specific information from:

Resumes
Company documents
Research papers
Technical documentation
Employee handbooks
Project documents

The objective of this project is to create a document assistant that allows users to upload documents and ask questions about their content.

Instead of manually searching through the entire document, the system retrieves relevant information and generates an answer.

Proposed Solution

The system follows this workflow:

User
 |
 v
Upload Document
 |
 v
File Validation
 |
 v
Document Processing
 |
 v
Text Extraction
 |
 v
Text Cleaning
 |
 v
Text Chunking
 |
 v
TF-IDF Retrieval
 |
 v
User Question
 |
 v
Relevant Document Chunks
 |
 v
AI Service
 |
 v
Generated Answer

The document viewing workflow is:

User
 |
 v
GET /documents
 |
 v
Uploaded Documents
 |
 v
Extracted Content
 |
 v
Display Document Content
System Architecture
                         USER
                           |
                           v
                    FASTAPI APPLICATION
                           |
              +------------+------------+
              |                         |
              v                         v
        POST /upload              GET /documents
              |                         |
              v                         v
       File Validation            Read Documents
              |                         |
              v                         v
       Save Document             Extract Content
              |                         |
              v                         |
      Document Processor               |
              |                         |
              v                         |
         Text Cleaning                 |
              |                         |
              v                         |
          Chunking <-------------------+
              |
              v
       DocumentChunk
              |
              v
       TF-IDF Retriever
              |
              v
           POST /ask
              |
              v
     Retrieve Relevant Chunks
              |
              v
         AI Service
              |
              v
            Answer
Project Workflow
Step 1: Upload Document

The user uploads a PDF, DOCX, or TXT file using:

POST /upload

The application validates and saves the file.

Step 2: Extract Text

The system extracts text based on the file extension:

PDF  -> PyPDF
DOCX -> python-docx
TXT  -> Python
Step 3: Clean Text

The extracted content is cleaned by removing unnecessary empty lines and whitespace.

Step 4: Create Chunks

The document is divided into smaller pieces.

Large Document
      |
      +-- Chunk 1
      +-- Chunk 2
      +-- Chunk 3
      +-- Chunk 4
      +-- ...
Step 5: Build Retrieval Index

TF-IDF converts document chunks into vectors.

Step 6: Ask Question

The user sends a question using:

POST /ask
Step 7: Retrieve Information

The question is converted into a TF-IDF vector and compared with document chunks using cosine similarity.

Step 8: Generate Answer

The most relevant chunks are provided to the AI service to generate the final answer.

Technology Stack
Technology	Purpose
Python	Main programming language
FastAPI	REST API framework
Uvicorn	Application server
Pydantic	Data validation
PyPDF	PDF text extraction
python-docx	DOCX text extraction
Scikit-learn	TF-IDF and cosine similarity
Pytest	Automated testing
python-dotenv	Environment variables
Project Structure
Day-29/
|
|-- app.py
|-- ai_service.py
|-- config.py
|-- document_processor.py
|-- models.py
|-- retriever.py
|-- requirements.txt
|-- pytest.ini
|-- .env
|
|-- documents/
|   |-- uploaded documents
|
|-- logs/
|   |-- application logs
|
|-- tests/
|   |-- conftest.py
|   |-- test_api.py
|   |-- test_document_processor.py
|   |-- test_retriever.py
|
`-- venv/
Important Files
app.py

The main FastAPI application.

It handles:

Document upload
Document listing
Document content retrieval
Question answering
Health checking
document_processor.py

Responsible for:

Reading TXT files
Reading PDF files
Reading DOCX files
Extracting text
Cleaning text
Creating document chunks
Storing chunk metadata
retriever.py

Responsible for:

TF-IDF vectorization
Cosine similarity
Ranking document chunks
Returning relevant chunks
ai_service.py

Responsible for generating answers using the configured AI service.

models.py

Contains Pydantic models used by the API.

config.py

Contains application configuration and environment settings.

tests/

Contains automated tests for the API, document processor, and retriever.

API Endpoints
GET /

Checks whether the application is running.

GET /
GET /health

Returns the health status of the application.

GET /health

Example:

{
  "status": "healthy"
}
POST /upload

Uploads a document.

Supported formats:

.pdf
.docx
.txt

Example:

POST /upload

The endpoint:

Validates the file.
Saves the file.
Extracts its content.
Cleans the text.
Creates chunks.
Adds chunks to the retrieval system.
GET /documents

Returns uploaded documents and their extracted content.

GET /documents

Example:

{
  "total_documents": 1,
  "documents": [
    {
      "filename": "example.txt",
      "file_type": ".txt",
      "size_bytes": 100,
      "content": "This is my document content."
    }
  ],
  "total_chunks": 1
}

This feature allows the user to verify that the document was uploaded and processed correctly.

POST /ask

Allows the user to ask questions about uploaded documents.

Example request:

{
  "question": "What is this document about?"
}

The system:

Receives the question.
Searches document chunks.
Calculates similarity.
Selects relevant chunks.
Sends relevant information to the AI service.
Returns the generated answer.
Document Processing

The document processor supports three formats.

TXT

TXT files are read using UTF-8 encoding.

PDF

PDF text is extracted using PyPDF.

DOCX

DOCX text is extracted using python-docx.

The processing pipeline is:

Document
   |
   v
Read File
   |
   v
Extract Text
   |
   v
Clean Text
   |
   v
Create Chunks
DocumentChunk

Each processed document is divided into chunks.

A chunk contains text and metadata.

Example:

DocumentChunk(
    text="Python is a programming language.",
    metadata={
        "chunk_index": 0
    }
)

Using DocumentChunk makes it possible to store additional information such as:

Filename
Chunk index
Page number
Document ID
Upload information
TF-IDF Retrieval

TF-IDF stands for:

Term Frequency - Inverse Document Frequency

It is used to determine the importance of words within documents.

The retrieval process is:

Document Chunks
      |
      v
TF-IDF Vectorization
      |
      v
Numerical Vectors

When the user asks a question:

User Question
      |
      v
TF-IDF Vector
      |
      v
Cosine Similarity
      |
      v
Rank Document Chunks
      |
      v
Top Relevant Chunks
Cosine Similarity

Cosine similarity measures how similar the user's question is to each document chunk.

A higher similarity score means that the chunk is more relevant.

The retriever ranks the results from highest similarity to lowest similarity.

Example:

scores.argsort()[::-1]
Question Answering Flow

Example question:

What skills does Rahul have?

The system performs:

Question
   |
   v
TF-IDF Vectorization
   |
   v
Cosine Similarity
   |
   v
Relevant Document Chunks
   |
   v
AI Service
   |
   v
Generated Answer
Document Viewing Feature

A new feature was added to allow users to view the actual content of uploaded documents.

Endpoint:

GET /documents

The response provides:

Filename
File Type
File Size
Extracted Content

Example:

{
  "filename": "resume.pdf",
  "file_type": ".pdf",
  "size_bytes": 24567,
  "content": "Rahul Rode..."
}
Benefit

This feature provides transparency and allows users to verify that the uploaded document was processed correctly.

Validation and Error Handling

The application handles common errors.

Unsupported File

Files other than PDF, DOCX, and TXT are rejected.

Examples:

.exe
.zip
.jpg
.png
Empty File

Empty uploaded files are rejected.

Empty Question

An empty question is rejected.

Missing Document

The application handles missing documents.

Invalid Input

FastAPI and Pydantic are used for request validation.

Installation
Step 1: Open the project directory
cd Day-29
Step 2: Create virtual environment
python -m venv venv
Step 3: Activate virtual environment

For Windows PowerShell:

.\venv\Scripts\Activate.ps1
Step 4: Install dependencies
pip install -r requirements.txt
Environment Variables

Create a .env file in the project root.

Example:

GOOGLE_API_KEY=your_api_key_here

Use the environment variables required by the AI service configured in the project.

Never commit API keys or other secrets to GitHub.

Running the Application

Start the FastAPI server:

uvicorn app:app --reload

The application will run at:

http://127.0.0.1:8000

Swagger API documentation:

http://127.0.0.1:8000/docs
How to Use the Application
Step 1: Start the server
uvicorn app:app --reload
Step 2: Open Swagger UI

Open:

http://127.0.0.1:8000/docs
Step 3: Check application health

Use:

GET /health
Step 4: Upload a document

Use:

POST /upload

Upload a PDF, DOCX, or TXT file.

Step 5: View uploaded documents

Use:

GET /documents

The response displays the uploaded document and its extracted content.

Step 6: Ask a question

Use:

POST /ask

Example:

{
  "question": "What is this document about?"
}
Step 7: View the answer

The system retrieves relevant document chunks and generates an answer.

Live Demo Flow

The recommended live demonstration is:

Start Application
       |
       v
Open Swagger UI
       |
       v
Check /health
       |
       v
Upload Document
       |
       v
GET /documents
       |
       v
Show Extracted Content
       |
       v
Ask Question
       |
       v
Show Generated Answer
       |
       v
Run Pytest
       |
       v
Show 21 Passed Tests
Testing

The project uses Pytest for automated testing.

Run:

pytest -v

Current test result:

21 passed, 1 warning
API Tests

The API tests verify:

Root endpoint
Health endpoint
Document upload
Document listing
Document content retrieval
Empty question
Invalid file
Empty file
Document Processor Tests

The tests verify:

Text cleaning
Text chunking
DocumentChunk
Chunk metadata
TXT document reading
Unsupported document handling
Retriever Tests

The tests verify:

Retriever initialization
Empty retriever
Search
Result metadata
Top-K retrieval
Test Result

Latest test execution:

============================= test session starts =============================

collected 21 items

21 passed, 1 warning

============================== 21 passed ==============================

The document content feature is specifically tested by:

test_get_document_content PASSED

This confirms that uploaded document content can be retrieved through the API.

Challenges Faced
Challenge 1: DocumentChunk Import Error

The retriever expected a DocumentChunk class, but the document processor initially returned plain strings.

Error:

ImportError: cannot import name 'DocumentChunk'

Solution:

A DocumentChunk structure was added to document_processor.py.

@dataclass
class DocumentChunk:
    text: str
    metadata: dict

The chunking function was updated to return DocumentChunk objects.

Challenge 2: Retriever Ranking

The retriever needed to rank similarity scores from highest to lowest.

The ranking was corrected to:

scores.argsort()[::-1]
Challenge 3: Pytest Import Error

Initially, pytest could not import:

app
document_processor
retriever

Error:

ModuleNotFoundError: No module named 'app'

Solution:

A pytest.ini configuration was added:

[pytest]
pythonpath = .
testpaths = tests

A tests/conftest.py file was also added to make the project root available during testing.

Project Improvements

The project was improved in the following areas.

Functionality
Added document content viewing.
Improved document processing.
Added document chunk metadata.
Improved retrieval.
Added file validation.
Testing
Added API tests.
Added document processor tests.
Added retriever tests.
Added error-handling tests.
Added document-content verification.
Reliability
Added file type validation.
Added empty-file validation.
Added empty-question validation.
Added health check.
Added automated testing.
Documentation
Added architecture documentation.
Documented API endpoints.
Documented installation.
Documented testing.
Documented challenges.
Documented future improvements.
Security Considerations

For production deployment, the following security improvements should be considered:

File size limits
File type validation
Filename sanitization
Authentication
Authorization
API rate limiting
Secure API key storage
Malware scanning
User-specific document access
HTTPS
Future Improvements
Vector Database

The current TF-IDF retrieval system can be replaced or extended with a vector database such as:

ChromaDB
FAISS
Pinecone
Semantic Search

Embedding models can be added for better semantic retrieval.

Authentication

User authentication can be added so every user can manage their own documents.

Document Management

Future functionality can include:

DELETE /documents/{filename}

for deleting uploaded documents.

Frontend

A frontend can be created using:

React
Streamlit

The frontend could provide:

File upload
Document list
Document content viewer
Chat interface
Answer history
Multi-Document Question Answering

The system can be extended to answer questions across multiple uploaded documents.

Cloud Deployment

The application can be deployed using:

Docker
AWS
Azure
Render
Demo Checklist

Before presenting the project, verify:

 Virtual environment is activated
 Dependencies are installed
 .env is configured
 Application starts successfully
 Swagger UI opens
 /health works
 PDF upload works
 DOCX upload works
 TXT upload works
 /documents works
 Uploaded document content is visible
 /ask works
 Relevant information is retrieved
 Answer is generated
 pytest -v passes
 README is ready
 PPT is ready
 Architecture diagram is ready
 Technical interview questions are prepared
 Demo video is ready
Presentation Flow

The project can be presented in approximately 10–15 minutes.

Recommended presentation structure:

Project Introduction
Problem Statement
Proposed Solution
Key Features
Technology Stack
System Architecture
Document Processing
TF-IDF Retrieval
Document Content Viewing Feature
API Demonstration
Testing Results
Challenges
Future Improvements
Conclusion
Technical Interview Questions

Possible technical questions related to this project:

Why did you choose FastAPI?
How does document processing work?
Why did you use TF-IDF?
What is cosine similarity?
Why is document chunking required?
How does the /ask endpoint work?
How does the application support different document formats?
How did you handle invalid files?
How did you test the project?
What improvements would you make for production?
Project Outcome

The final system provides a complete document question-answering workflow:

                 DOCUMENT
                     |
                     v
                  UPLOAD
                     |
                     v
              TEXT EXTRACTION
                     |
                     v
                TEXT CLEANING
                     |
                     v
                  CHUNKING
                     |
                     v
               TF-IDF INDEX
                     |
                     v
                  QUESTION
                     |
                     v
             RELEVANT CHUNKS
                     |
                     v
                AI SERVICE
                     |
                     v
                  ANSWER

The system also provides document content viewing:

GET /documents
       |
       v
Uploaded Documents
       |
       v
Extracted Content
Conclusion

The AI Document Question Answering System demonstrates how FastAPI, document processing, information retrieval, and AI services can be combined to build a practical document assistant.

The application supports PDF, DOCX, and TXT document uploads, extracts their content, processes documents into chunks, retrieves relevant information, and generates answers to user questions.

A document viewing feature was added so users can see the actual extracted content of uploaded documents.

The project includes automated testing using Pytest, with 21 tests currently passing.

The system provides a strong foundation for future improvements such as semantic embeddings, vector databases, authentication, frontend development, multi-user support, and cloud deployment.

Author

Rahul Rode

AI / Machine Learning Project

Technologies Used
Python
FastAPI
Uvicorn
PyPDF
python-docx
Scikit-learn
Pydantic
Pytest
python-dotenv