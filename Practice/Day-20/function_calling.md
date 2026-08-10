# Function Calling Documentation

## 1. Introduction

Function calling allows the AI model to select and use
external functions when the user's request requires a
specific operation.

The model does not directly execute the Python function.
The application provides the function and executes it
when the model requests it.

## 2. Function Calling Workflow

User Request
     |
     v
Gemini Model
     |
     v
Select Appropriate Tool
     |
     v
Call Python Function
     |
     v
Tool Executes
     |
     v
Tool Result
     |
     v
Gemini Model
     |
     v
Final Answer

## 3. Available Tools

### Calculator

Function:

calculator(expression)

Purpose:

Performs mathematical calculations.

Example:

calculator("25 * 10")

---

### Web Search

Function:

web_search(query)

Purpose:

Searches the web for information.

Example:

web_search("latest AI news")

---

### Database Tool

Function:

database_query(query)

Purpose:

Executes read-only SQL SELECT queries.

Example:

database_query(
    "SELECT * FROM employees"
)

Only SELECT queries are allowed.

---

### File Reader

Function:

read_file(file_path)

Purpose:

Reads TXT, CSV, JSON, Markdown and PDF files.

Example:

read_file("sample_data/company.txt")

---

### Weather Tool

Function:

get_weather(city)

Purpose:

Gets current weather information.

Example:

get_weather("Pune")

---

### Email Tool

Function:

send_email(
    recipient,
    subject,
    message
)

Purpose:

Processes an email request.

The current implementation simulates email sending
to prevent accidental real-world email delivery.

---

### Date Tool

Function:

date_tool(
    operation,
    date1,
    date2
)

Purpose:

Performs date operations.

Supported operations:

- today
- difference

---

### Data Analyzer

Function:

analyze_data(file_path)

Purpose:

Analyzes CSV datasets.

It calculates:

- Number of rows
- Number of columns
- Missing values
- Average
- Minimum
- Maximum

---

### Company PDF Reader

Function:

company_pdf_reader(file_path)

Purpose:

Reads company PDF documents.

This is the practical project tool.

## 4. Tool Selection

The AI selects tools according to the user's intent.

Examples:

"What is 20 + 30?"

Tool:

Calculator

"Show IT employees."

Tool:

Database Tool

"Analyze sales.csv."

Tool:

Data Analyzer

"What is the weather in Pune?"

Tool:

Weather Tool

"Tell me the leave policy from the handbook."

Tool:

Company PDF Reader

## 5. Tool Chaining

Tools can be used sequentially.

Example:

User:

"Find the IT employees and calculate their average salary."

Possible workflow:

User Request
     |
     v
Database Tool
     |
     v
Employee Salary Data
     |
     v
Calculation / Data Analysis
     |
     v
Final Answer

## 6. Error Handling

Each tool handles errors.

Examples:

Calculator:

Division by zero.

Database:

Invalid SQL query.

File Reader:

Missing file.

Weather:

City not found.

Date:

Invalid date format.

Data Analyzer:

Invalid CSV.

PDF Reader:

Unreadable PDF.

Email:

Invalid email address.

## 7. Security

The database tool only accepts SELECT queries.

The email tool is simulated.

The calculator does not use Python eval().

API keys are stored in .env.

The virtual environment is excluded from Git.

## 8. Conclusion

Function calling allows the AI assistant to extend its
capabilities beyond normal text generation.

The AI can select the correct tool based on the user's
request and use the result to generate a final answer.