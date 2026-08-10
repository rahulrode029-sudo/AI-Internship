# AI Tool-Calling Assistant

## Project Overview

This project demonstrates the implementation of an AI Tool-Calling Assistant using Python and the Gemini API.

The main objective is to understand how an AI agent can identify a user's intent, select the appropriate tool, execute a function, process the tool result, and generate a final response.

The project covers tool creation, function calling, tool chaining, error handling, tool selection, and a practical company PDF reader tool.

---

## Learning Objectives

The project focuses on the following concepts:

* Tool Creation
* Function Calling
* Tool Chaining
* Error Handling
* Tool Selection
* Function Calling Decision Making
* AI Agent Workflow
* Company Document Processing

---

## Tools Implemented

The project contains the following tools:

1. Calculator
2. Web Search
3. Database Tool
4. File Reader
5. Weather Tool
6. Email Tool
7. Date Tool
8. Data Analyzer
9. Company PDF Reader

---

## Project Structure

```text
Day-20/
|
├── tools/
│   ├── __init__.py
│   ├── calculator.py
│   ├── web_search.py
│   ├── database_tool.py
│   ├── file_reader.py
│   ├── weather_tool.py
│   ├── email_tool.py
│   ├── date_tool.py
│   └── data_analyzer.py
|
├── project_tool/
│   ├── __init__.py
│   └── pdf_reader_tool.py
|
├── database/
│   └── company.db
|
├── sample_data/
│   ├── employees.csv
│   ├── company.txt
│   └── Employee_Handbook.pdf
|
├── main.py
├── test_tools.py
├── create_database.py
├── decision_matrix.md
├── function_calling.md
├── workflow_notes.md
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Technologies Used

* Python 3.12
* Gemini API
* Google GenAI SDK
* SQLite
* Pandas
* PyPDF
* Requests
* DuckDuckGo Search
* Python-dotenv

---

## Virtual Environment

A Python virtual environment is used to isolate project dependencies.

Create the virtual environment:

```bash
python -m venv venv
```

For Python 3.12:

```bash
py -3.12 -m venv venv
```

Activate the virtual environment on Windows:

```powershell
venv\Scripts\activate
```

After activation, the terminal should show:

```text
(venv)
```

---

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

The main dependencies are:

```text
google-genai
python-dotenv
requests
pandas
pypdf
duckduckgo-search
```

---

## Gemini API Configuration

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

Replace `YOUR_GEMINI_API_KEY` with your actual Gemini API key.

The `.env` file should not be committed to GitHub.

The `.gitignore` file contains:

```text
venv/
.env
__pycache__/
*.pyc
*.db
```

---

# Database Setup

The project uses SQLite for the Database Tool.

Run:

```bash
python create_database.py
```

The command creates:

```text
database/company.db
```

The database contains an `employees` table with information such as:

* Employee ID
* Name
* Department
* Position
* Salary

Example database query:

```sql
SELECT name, department, salary
FROM employees;
```

Only read-only `SELECT` queries are allowed by the Database Tool.

---

# Running the Individual Tools

Before running the AI assistant, the individual tools can be tested.

Run:

```bash
python test_tools.py
```

This tests:

* Calculator
* Database Tool
* File Reader
* Weather Tool
* Email Tool
* Date Tool
* Data Analyzer
* Company PDF Reader

---

# Running the AI Assistant

Start the main application:

```bash
python main.py
```

The application provides the following tools:

```text
1. Calculator
2. Web Search
3. Database
4. File Reader
5. Weather
6. Email
7. Date
8. Data Analyzer
9. Company PDF Reader
```

The user can enter a natural-language request.

Example:

```text
What is 25 multiplied by 40?
```

The AI identifies that the Calculator Tool is required and calls the appropriate function.

---

# Example User Requests

## Calculator

```text
What is 25 multiplied by 40?
```

Expected tool:

```text
Calculator
```

---

## Web Search

```text
Search for the latest information about artificial intelligence.
```

Expected tool:

```text
Web Search
```

---

## Database

```text
Show all employees in the IT department.
```

Expected tool:

```text
Database Tool
```

---

## File Reader

```text
Read sample_data/company.txt.
```

Expected tool:

```text
File Reader
```

---

## Weather

```text
What is the weather in Pune?
```

Expected tool:

```text
Weather Tool
```

---

## Email

```text
Send an email to HR saying that I will be late.
```

Expected tool:

```text
Email Tool
```

The current implementation simulates email sending for testing purposes.

---

## Date

```text
What is today's date?
```

Expected tool:

```text
Date Tool
```

Another example:

```text
How many days are there between 2026-08-01 and 2026-08-15?
```

Expected result:

```text
14 days
```

---

## Data Analyzer

```text
Analyze sample_data/employees.csv.
```

Expected tool:

```text
Data Analyzer
```

The analyzer provides:

* Number of rows
* Number of columns
* Column names
* Missing values
* Average
* Minimum
* Maximum

---

## Company PDF Reader

```text
What is the leave policy in Employee_Handbook.pdf?
```

Expected tool:

```text
Company PDF Reader
```

The tool extracts text from the company PDF document and provides the information to the AI.

---

# Function Calling

Function calling allows the AI model to select an external function when a user's request requires a specific operation.

The general workflow is:

```text
User Request
     |
     v
AI Model
     |
     v
Understand User Intent
     |
     v
Select Appropriate Tool
     |
     v
Call Python Function
     |
     v
Execute Function
     |
     v
Tool Result
     |
     v
AI Model
     |
     v
Final Answer
```

For example:

```text
User:
What is 100 / 5?

AI:
Select Calculator Tool

Calculator:
100 / 5 = 20

AI:
The answer is 20.
```

---

# Tool Selection

The AI selects a tool according to the user's request.

| User Request                      | Tool               |
| --------------------------------- | ------------------ |
| What is 25 multiplied by 40?      | Calculator         |
| Search for the latest AI news.    | Web Search         |
| Show IT employees.                | Database Tool      |
| Read company.txt.                 | File Reader        |
| What is the weather in Pune?      | Weather Tool       |
| Send an email to HR.              | Email Tool         |
| What is today's date?             | Date Tool          |
| Analyze employees.csv.            | Data Analyzer      |
| What is the company leave policy? | Company PDF Reader |

A detailed decision matrix is available in:

```text
decision_matrix.md
```

---

# Tool Chaining

Tool chaining occurs when more than one operation is required to complete a request.

Example:

```text
Find all IT employees and calculate their average salary.
```

Possible workflow:

```text
User Request
     |
     v
Database Tool
     |
     v
Retrieve IT Employee Salaries
     |
     v
Calculation/Data Analysis
     |
     v
Average Salary
     |
     v
Final Answer
```

Another example:

```text
Read employees.csv and calculate the average salary.
```

Workflow:

```text
User
 |
 v
Data Analyzer
 |
 v
Read CSV
 |
 v
Analyze Salary
 |
 v
Calculate Average
 |
 v
Final Answer
```

---

# Error Handling

Error handling has been implemented in the tools to prevent the application from crashing.

Examples include:

### Calculator

Handles:

* Division by zero
* Invalid mathematical expressions
* Unsupported operations

### Database

Handles:

* Empty queries
* Invalid SQL
* Non-SELECT queries
* Database errors

### File Reader

Handles:

* Missing files
* Empty files
* Unsupported file formats
* File reading errors

### Weather

Handles:

* Invalid city names
* Network errors
* API errors

### Email

Handles:

* Missing recipient
* Invalid email address
* Missing subject
* Missing message

### Date

Handles:

* Invalid dates
* Invalid date format
* Unsupported operations

### Data Analyzer

Handles:

* Missing CSV files
* Empty files
* Unsupported file formats
* Invalid CSV data

### Company PDF Reader

Handles:

* Missing PDF files
* Unsupported file formats
* Empty PDFs
* PDFs without readable text

---

# Practical Project

## Company PDF Reader

The Company PDF Reader was selected as the practical company tool.

The purpose of this tool is to allow the AI assistant to read company documents and use their contents to answer employee questions.

Example:

```text
User:
What is the leave policy?

        |

        v

AI Assistant

        |

        v

Company PDF Reader

        |

        v

Employee_Handbook.pdf

        |

        v

Extract Text

        |

        v

AI Model

        |

        v

Final Answer
```

This tool can be further integrated with a RAG pipeline.

---

# Future RAG Integration

The Company PDF Reader can be extended into a complete company-document RAG system.

The future architecture can be:

```text
Company PDF
     |
     v
Text Extraction
     |
     v
Document Chunking
     |
     v
Embeddings
     |
     v
Vector Database
     |
     v
Semantic Retrieval
     |
     v
Gemini LLM
     |
     v
Company AI Assistant
```

This would allow the assistant to answer questions from multiple company documents while retrieving only relevant information.

---

# Testing

The project was tested using individual tool execution and AI-based function calling.

Basic tool testing:

```bash
python test_tools.py
```

Database testing:

```bash
python create_database.py
```

AI assistant testing:

```bash
python main.py
```

Example test cases:

```text
What is 25 * 40?

Show all employees in IT.

What is the weather in Pune?

Analyze employees.csv.

Read company.txt.

What is today's date?

What is the leave policy in the employee handbook?

Calculate 10 / 0.
```

---

# Issue Encountered

During AI assistant testing, the following error was encountered:

```text
404 NOT_FOUND

This model models/gemini-2.5-flash is no longer available to new users.
```

## Cause

The configured Gemini model was not available for the current API account.

The problem was related to model availability and not to the tool implementation.

## Resolution

The available Gemini models should be checked using the Gemini SDK and the model configuration should be updated to a model supported by the API key.

The model is configured in:

```text
main.py
```

Example:

```python
model="AVAILABLE_MODEL_NAME"
```

---

# Deliverables

The following deliverables were completed:

1. Tool Selection Matrix
2. Function Calling Documentation
3. Workflow Notes
4. Calculator Tool
5. Web Search Tool
6. Database Tool
7. File Reader
8. Weather Tool
9. Email Tool
10. Date Tool
11. Data Analyzer
12. Company PDF Reader
13. Error Handling
14. Tool Testing
15. Function Calling Implementation

---

# Key Learning Outcomes

Through this project, the following concepts were understood:

* How to create reusable AI tools
* How function calling works
* How an AI model selects tools
* How tool arguments are passed
* How tool results are returned to the model
* How multiple tools can be chained
* How to handle tool execution errors
* How to connect an AI assistant with databases and files
* How to build a company-specific AI tool
* How tool calling can be combined with RAG systems

---

# Conclusion

The AI Tool-Calling Assistant demonstrates how an AI agent can extend its capabilities by using external tools.

Instead of generating every answer directly, the AI can identify when a calculation, database query, web search, file operation, weather lookup, date operation, data analysis, email operation, or company document lookup is required.

The project provides a foundation for building more advanced AI agents that combine function calling, tool chaining, RAG, databases, APIs, and company-specific knowledge.
