# Workflow Notes

## Objective

The objective of this project is to demonstrate tool
creation, function calling, tool chaining and error
handling using an AI assistant.

## Overall Workflow

User
 |
 v
AI Assistant
 |
 v
Understand User Intent
 |
 v
Select Tool
 |
 +-----------------------------+
 |                             |
 v                             v
Single Tool                 Multiple Tools
 |                             |
 v                             v
Execute Tool                Tool 1
 |                             |
 v                             v
Tool Result                 Tool 2
 |                             |
 +-------------+---------------+
               |
               v
          AI Processing
               |
               v
          Final Answer

## Tool Selection

The AI selects tools based on the user's request.

Examples:

Calculation request
        |
        v
Calculator

Database request
        |
        v
Database Tool

File request
        |
        v
File Reader

Weather request
        |
        v
Weather Tool

Email request
        |
        v
Email Tool

Date request
        |
        v
Date Tool

CSV analysis request
        |
        v
Data Analyzer

Company document request
        |
        v
Company PDF Reader

## Tool Chaining

Tool chaining is used when a request requires multiple
operations.

Example:

"Find all IT employees and calculate their average salary."

Step 1:
Database Tool retrieves IT employee records.

Step 2:
Salary values are processed.

Step 3:
Average salary is calculated.

Step 4:
AI generates the final response.

## Error Handling

The application handles:

- Missing files
- Empty files
- Unsupported files
- Invalid database queries
- Division by zero
- Invalid dates
- Invalid email addresses
- Network errors
- API errors
- Missing API keys

## Practical Project

The selected practical tool is the Company PDF Reader.

It allows the AI assistant to read company documents
and answer questions based on their contents.

Workflow:

User Question
      |
      v
AI Assistant
      |
      v
Company PDF Reader
      |
      v
Extract PDF Text
      |
      v
AI
      |
      v
Final Answer