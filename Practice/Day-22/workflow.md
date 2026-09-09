# Multi-Agent Research Assistant - Workflow

## 1. Workflow Overview

The Multi-Agent AI Research Assistant follows a sequential workflow with a feedback loop.

The workflow converts a user's research question into a final structured response.

The overall process is:

```text
User
 ↓
Coordinator
 ↓
Research Agent
 ↓
Analyzer
 ↓
Critic
 ↓
Writer
 ↓
Coordinator
 ↓
User
```

If the Critic identifies problems, the workflow returns to the Analyzer for revision.

---

## 2. Step-by-Step Workflow

### Step 1 - User Query

The user enters a research question.

Example:

```text
What are the benefits and challenges of artificial intelligence in healthcare?
```

The query becomes the initial input to the system.

---

### Step 2 - Coordinator

The Coordinator receives the user query.

The Coordinator creates a research plan.

Example:

```text
1. Identify applications of AI in healthcare.
2. Identify major benefits.
3. Identify risks and challenges.
4. Analyze the collected information.
5. Prepare a structured response.
```

The research plan is stored in the shared state.

---

### Step 3 - Research Agent

The Research Agent receives:

```text
User Query
Research Plan
```

It generates research notes containing relevant information.

The output is stored as:

```text
research_results
```

The workflow then moves to the Analyzer.

---

### Step 4 - Analyzer

The Analyzer receives the research results.

It processes the information by:

* Organizing the findings.
* Identifying important information.
* Removing irrelevant information.
* Comparing findings.
* Identifying advantages.
* Identifying challenges.
* Identifying possible weaknesses.

The result is stored as:

```text
analysis
```

The workflow moves to the Critic.

---

### Step 5 - Critic

The Critic receives the analysis.

It checks:

```text
Relevance
Logical consistency
Completeness
Unsupported claims
Missing information
Overall quality
```

The Critic produces one of two decisions.

### Decision 1 - Approve

```text
DECISION: APPROVE
```

The workflow moves to the Writer.

### Decision 2 - Revise

```text
DECISION: REVISE
```

The Critic provides feedback.

The workflow returns to the Analyzer.

---

## 3. Revision Loop

The revision workflow is:

```text
Analyzer
    |
    v
Critic
    |
    | REVISE
    v
Analyzer
    |
    v
Critic
```

The Analyzer uses the Critic's feedback to improve the analysis.

The revised analysis is sent to the Critic again.

A maximum revision count is used to prevent an infinite loop.

---

## 4. Writer

When the Critic approves the analysis, the Writer receives:

```text
User Query
Approved Analysis
Critic Feedback
```

The Writer generates the final response.

The Writer does not expose internal workflow information to the user.

---

## 5. Final Response

The Writer sends the final answer back through the workflow.

```text
Writer
   ↓
Coordinator
   ↓
User
```

The Coordinator completes the workflow.

---

## 6. Complete Workflow Diagram

```text
                         USER
                           |
                           v
                    +-------------+
                    | COORDINATOR |
                    +-------------+
                           |
                     Research Plan
                           |
                           v
                    +-------------+
                    |  RESEARCHER |
                    +-------------+
                           |
                    Research Results
                           |
                           v
                    +-------------+
                    |   ANALYZER  |
                    +-------------+
                           |
                        Analysis
                           |
                           v
                    +-------------+
                    |    CRITIC   |
                    +-------------+
                       /       \
                      /         \
                 APPROVE       REVISE
                    |             |
                    v             v
                +--------+    +---------+
                | WRITER |    | ANALYZER|
                +--------+    +---------+
                    |             |
                    |             v
                    |          CRITIC
                    |             |
                    +-------------+
                           |
                           v
                    +-------------+
                    | COORDINATOR |
                    +-------------+
                           |
                           v
                          USER
```

---

## 7. Shared State During Workflow

The shared state changes as the workflow progresses.

### Initial State

```text
user_query
research_plan = []
research_results = ""
analysis = ""
critic_feedback = ""
revision_count = 0
final_answer = ""
workflow_status = "Started"
```

### After Coordinator

```text
research_plan = [...]
workflow_status = "Research plan created"
```

### After Research Agent

```text
research_results = "..."
workflow_status = "Research completed"
```

### After Analyzer

```text
analysis = "..."
workflow_status = "Analysis completed"
```

### After Critic

```text
critic_feedback = "..."
workflow_status = "Analysis reviewed"
```

### After Writer

```text
final_answer = "..."
workflow_status = "Final answer generated"
```

---

## 8. Workflow Decision Logic

The Critic determines the next step.

Conceptually:

```python
if critic_approves:
    next_agent = "writer"
else:
    next_agent = "analyzer"
```

A revision limit is also applied.

```text
If revisions < maximum:
    Analyzer → Critic

If maximum revisions reached:
    Critic → Writer
```

This prevents the workflow from running indefinitely.

---

## 9. Agent Communication Flow

The communication flow is:

```text
User
 ↓
Coordinator
 │
 │ Research Plan
 ↓
Research Agent
 │
 │ Research Results
 ↓
Analyzer
 │
 │ Analysis
 ↓
Critic
 │
 ├── Revision Feedback ──→ Analyzer
 │
 └── Approval ───────────→ Writer
                              │
                              │ Final Answer
                              v
                         Coordinator
                              |
                              v
                             User
```

---

## 10. Example Execution

For the question:

```text
What are the benefits and challenges of AI in education?
```

The system performs:

```text
1. Coordinator receives the question.

2. Coordinator creates a research plan.

3. Research Agent produces research notes.

4. Analyzer organizes the research.

5. Critic reviews the analysis.

6. If problems are found, the Analyzer revises the analysis.

7. Critic reviews the revised analysis.

8. Once approved, Writer creates the final response.

9. Coordinator returns the response to the user.
```

---

## 11. Workflow Status

The system tracks the current workflow using:

```text
Started
Research plan created
Research completed
Analysis completed
Analysis reviewed
Final answer generated
```

This makes it easier to monitor and debug the workflow.

---

## 12. Error and Failure Handling

The current implementation uses basic safeguards.

### Empty Query

If the user does not enter a question, the application displays an error message and stops.

### Critic Loop

A revision counter limits the number of Analyzer-Critic cycles.

### API Key

The application checks whether the Gemini API key is available.

### Model Failure

If the language model cannot be accessed, the application will return an error that can be handled during testing.

---

## 13. Testing Workflow

The application should be tested using different research questions.

### Test Case 1

```text
What are the benefits of artificial intelligence in healthcare?
```

### Test Case 2

```text
What are the advantages and disadvantages of cloud computing?
```

### Test Case 3

```text
How can AI improve customer support?
```

For each test, verify:

* Coordinator creates a plan.
* Research Agent produces research.
* Analyzer creates analysis.
* Critic reviews the analysis.
* Revision occurs when required.
* Writer generates the final response.
* Final response is returned successfully.

---

## 14. Expected Result

The expected result is a clear final answer generated after the research, analysis, and quality-control stages.

The user should only see the final answer, while the internal agent workflow remains controlled by the application.

---

## 15. Conclusion

The workflow demonstrates how multiple specialized AI agents can collaborate to complete a complex research task.

The Coordinator manages the process, the Research Agent gathers information, the Analyzer processes the information, the Critic validates the analysis, and the Writer produces the final response.

The Critic feedback loop provides an additional quality-control mechanism and demonstrates how multi-agent systems can iteratively improve their results.
