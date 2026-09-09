# Day-19 – LangGraph RAG Workflow

## 1. Project Overview

Day-19 focuses on **LangGraph**, a framework for building structured AI workflows using graphs and state management.

The main learning objectives of this task are:

* Nodes
* Graphs
* State
* Conditional Flow
* Memory

As the practical implementation, a **LangGraph-based RAG Question Answering System** is developed. The application accepts a user question, retrieves relevant information from documents, sends the retrieved context to a Gemini LLM, generates an answer, and maintains conversation memory.

The project also demonstrates conditional routing and error handling so that the workflow can recover when relevant information is not found.

---

## 2. Objectives

The primary objective is to understand how an AI application can be divided into multiple independent workflow steps using LangGraph.

The project demonstrates:

1. Creating nodes for individual tasks.
2. Connecting nodes using a graph.
3. Passing information between nodes using state.
4. Using conditional routing to make workflow decisions.
5. Maintaining conversation memory.
6. Handling possible workflow failures.
7. Building a simple RAG application using LangGraph.

The practical workflow is:

```text
User
  ↓
Question
  ↓
Retriever
  ↓
Conditional Routing
  ↓
LLM
  ↓
Answer
  ↓
Memory
```

---

# 3. LangGraph Concepts

## 3.1 Nodes

A node is an individual processing step in a LangGraph workflow.

In this project, different operations are separated into nodes. For example, the retrieval node searches the document collection, while the generation node uses the retrieved information to generate an answer.

This makes the application easier to understand, debug, and modify.

---

## 3.2 Graph

A graph defines how different nodes are connected.

Instead of executing all operations inside one large function, the application creates a workflow where each node performs a specific task.

The graph controls the movement of information between nodes.

Example:

```text
START
  ↓
Retrieve
  ↓
Generate
  ↓
Memory
  ↓
END
```

---

## 3.3 State

State is the shared information passed between nodes.

The application state can contain:

```text
question
documents
answer
history
error
```

For example, the user question is stored in the state by the starting part of the workflow. The retriever then adds relevant documents to the state. The LLM uses the question and documents to create the answer, which is also stored in the state.

Therefore, state acts as the communication mechanism between different nodes.

---

## 3.4 Conditional Flow

Conditional routing allows the graph to choose different paths depending on the current state.

For example, after retrieving documents, the workflow checks whether relevant documents were found.

```text
             Retriever
                 ↓
        Documents Found?
          /           \
        YES            NO
         ↓              ↓
       LLM        Error Handler
         ↓
       Answer
```

If relevant documents are found, the workflow continues to the LLM.

If no relevant documents are found, the workflow moves to an error-handling path.

---

## 3.5 Memory

Memory allows the application to maintain previous conversation information.

For example:

```text
User: Who is the CEO?

AI: The CEO is Rahul.

User: When did he join the company?

AI: He joined the company in 2020.
```

The second question depends on the previous conversation. Memory allows the workflow to maintain this context.

---

# 4. Project Practical – RAG Workflow

The practical task is to design the following workflow:

```text
User
 ↓
Question
 ↓
Retriever
 ↓
LLM
 ↓
Answer
 ↓
Memory
```

The project extends this basic workflow with conditional routing:

```text
                       User
                        ↓
                     Question
                        ↓
                    Retriever
                        ↓
              Documents Available?
                 /             \
               YES              NO
                ↓                ↓
               LLM        Error Handler
                ↓
              Answer
                ↓
              Memory
                ↓
                END
```

The application uses documents stored in the `documents` folder as its knowledge source.

The retriever searches the documents for information relevant to the user's question.

The retrieved context is then provided to the Gemini model so that the model can generate an answer based on the available information.

---

# 5. RAG Process

RAG stands for **Retrieval-Augmented Generation**.

The RAG process consists of three major steps.

### Retrieval

The system searches the document collection and finds relevant document chunks.

### Augmentation

The retrieved document information is combined with the user's question.

### Generation

The LLM uses the question and retrieved context to generate the final response.

The complete process is:

```text
Documents
    ↓
Document Chunks
    ↓
Embeddings
    ↓
Vector Database
    ↓
Retriever
    ↓
Relevant Context
    ↓
User Question + Context
    ↓
Gemini LLM
    ↓
Generated Answer
```

This approach allows the application to answer questions using information contained in the provided documents rather than relying only on the LLM's general knowledge.

---

# 6. Project Architecture

The architecture of the project is:

```text
                     +-------------+
                     |    USER     |
                     +------+------+
                            |
                            ↓
                     +-------------+
                     |  QUESTION   |
                     +------+------+
                            |
                            ↓
                     +-------------+
                     |  RETRIEVER  |
                     +------+------+
                            |
                            ↓
                 +----------------------+
                 | Documents Available? |
                 +----------+-----------+
                       YES  |  NO
                         |  |
                         ↓  ↓
                    +----+  +-------------+
                    | LLM|  |Error Handler|
                    +--+-+  +-------------+
                       |
                       ↓
                  +----------+
                  |  ANSWER  |
                  +----+-----+
                       |
                       ↓
                  +----------+
                  |  MEMORY  |
                  +----+-----+
                       |
                       ↓
                      END
```

Each component has a specific responsibility.

### User

The user provides a question.

### Retriever

The retriever searches the document collection for relevant information.

### Conditional Router

The router checks whether useful documents were retrieved.

### LLM

The LLM generates an answer using the question and retrieved context.

### Memory

Memory stores the conversation so that future questions can use previous context.

---

# 7. Project Structure

The Day-19 project contains the following files:

```text
Day-19/
│
├── documents/
│   └── company documents
│
├── venv/
│
├── app.py
├── graph.py
├── llm.py
├── memory.py
├── retriever.py
├── state.py
├── requirements.txt
├── .env
└── README.md
```

### app.py

The main entry point of the application.

It accepts a question from the user and invokes the LangGraph workflow.

### graph.py

Defines the LangGraph workflow and connects the nodes.

### retriever.py

Loads documents, creates embeddings, stores document vectors, and retrieves relevant documents.

### llm.py

Configures the Gemini LLM and generates answers using retrieved context.

### memory.py

Maintains conversation history.

### state.py

Defines the state shared by the LangGraph nodes.

### documents/

Contains the documents used by the RAG system.

### .env

Contains the Gemini API key.

The `.env` file should never be uploaded to GitHub.

---

# 8. Environment Setup

A virtual environment is used for this project to keep the project's dependencies separate from other Python projects.

Create the environment:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

Install the required libraries:

```bash
pip install langgraph langchain langchain-community langchain-google-genai langchain-huggingface langchain-text-splitters chromadb sentence-transformers python-dotenv
```

Save the installed packages:

```bash
pip freeze > requirements.txt
```

The Gemini API key is stored in `.env`:

```env
GOOGLE_API_KEY=your_api_key
```

The application loads this value using `python-dotenv`.

---

# 9. Workflow Execution

When the application starts, the user is asked to enter a question.

Example:

```text
Ask Question: Who is the CEO of the company?
```

The question enters the LangGraph workflow.

### Step 1 – Question

The user's question is stored in the graph state.

### Step 2 – Retrieval

The retriever searches the document collection.

### Step 3 – Conditional Routing

The graph checks whether relevant documents were found.

### Step 4 – Generation

If documents are found, the question and retrieved context are sent to the Gemini LLM.

### Step 5 – Answer

The generated response is stored in the state.

### Step 6 – Memory

The question and answer can be stored in conversation history.

### Step 7 – End

The final answer is returned to the user.

---

# 10. Workflow Analysis and Failure Scenario

One possible failure scenario is that the retriever cannot find relevant information in the available documents.

For example:

```text
User Question:
What is the company's stock price?

Retriever:
No relevant documents found.
```

If the workflow directly sends empty context to the LLM, the model may generate an incorrect or unsupported response.

Therefore, conditional routing is used.

```text
Retriever
    ↓
Documents Found?
    |
    +------ YES ------→ Generate Answer
    |
    +------ NO -------→ Error Handler
```

The error handler can return:

```text
No relevant information was found in the available documents.
Please try asking another question.
```

This allows the workflow to recover gracefully instead of crashing.

---

# 11. Error Handling Notes

Several failures are possible in a RAG workflow.

### No Documents Found

The retriever may return no relevant documents.

**Recovery:** Route the workflow to an error handler.

### Empty User Input

The user may submit an empty question.

**Recovery:** Validate the input before starting the graph.

### API Key Error

The Gemini API key may be missing or invalid.

**Recovery:** Check the `.env` file and provide a clear configuration error.

### API Failure

The Gemini service may temporarily fail because of network problems or service limitations.

**Recovery:** Use exception handling and optionally retry the operation.

### Invalid Document

A document may be empty, corrupted, or unsupported.

**Recovery:** Catch document-loading errors and notify the user.

---

# 12. Testing

The workflow should be tested using different inputs.

### Test Case 1 – Valid Question

```text
Who is the CEO of the company?
```

Expected result:

The retriever finds relevant information and the LLM generates an answer.

### Test Case 2 – Unknown Question

```text
What is the company's stock price?
```

Expected result:

The system should indicate that relevant information was not found.

### Test Case 3 – Empty Question

```text
```

Expected result:

```text
Please enter a valid question.
```

### Test Case 4 – Follow-up Question

```text
Who is the CEO?
```

Then:

```text
When did he join the company?
```

Expected result:

Memory should allow the system to understand the reference to the CEO.

---

# 13. Deliverables

The following deliverables are completed as part of the Day-19 task:

### 1. LangGraph Workflow

A graph-based RAG workflow containing retrieval, generation, conditional routing, and memory.

### 2. Workflow Analysis Report

A failure scenario is identified and a recovery mechanism is explained.

### 3. Updated LangGraph Diagram

The workflow diagram shows the relationship between the user, retriever, conditional routing, LLM, answer, and memory.

### 4. Error Handling Notes

Possible failures and their recovery mechanisms are documented.

---

# 14. Conclusion

The Day-19 project demonstrates how LangGraph can be used to build structured and reliable AI workflows.

The project implements the main concepts of:

* Nodes
* Graphs
* State
* Conditional Flow
* Memory
* Retrieval
* LLM generation
* Error handling

The final workflow is:

```text
User
 ↓
Question
 ↓
Retriever
 ↓
Conditional Routing
 ↓
LLM
 ↓
Answer
 ↓
Memory
```

Conditional routing improves reliability by allowing the application to handle situations such as missing documents or invalid input.

This project provides a foundation for building more advanced AI agents and multi-step workflows using LangGraph.


# 15. Questions for asking the model

Questions for your Day-19 model

Basic questions

What is the main purpose of this AI project?
What technologies are used in this project?
What is RAG?
What is LangGraph?
What is ChromaDB?
What are embeddings?
What is the role of the retriever?
What is the purpose of the documents folder?
What is the role of the LLM in this project?
What is the purpose of graph.py?

Day-wise questions
11. What was covered on Day 1?
12. What Machine Learning algorithm was used on Day 7?
13. What was the House Price Prediction project?
14. What was learned about NLP on Day 9?
15. Which Transformer model was used on Day 10?
16. What was the purpose of Day 11?
17. What database technology was learned on Day 12?
18. What was learned about model serialization on Day 13?
19. What was the main focus of Day 14?
20. What was built on Day 15?
21. What was learned about RAG on Day 16?
22. What was the purpose of the FastAPI RAG API on Day 17?
23. What was the focus of Day 18?
24. What was built using LangGraph on Day 19?

Specific project questions
25. What is the workflow of the Day-19 application?
26. How does the retriever find relevant information?
27. How are documents converted into embeddings?
28. Where are the document embeddings stored?
29. How does the system generate the final answer?
30. What is the role of state.py?
31. What is the role of memory.py?
32. What is the role of llm.py?
33. What is the role of retriever.py?
34. What is the role of app.py?
35. How does LangGraph connect the retriever and LLM?