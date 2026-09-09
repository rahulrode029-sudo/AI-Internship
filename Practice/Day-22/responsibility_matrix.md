# Multi-Agent Responsibility Matrix

## 1. Overview

The Multi-Agent AI Research Assistant divides the overall research task among five specialized AI agents.

Each agent has a specific responsibility, input, output, dependency, and communication path.

This responsibility matrix defines how the agents work together within the overall system.

---

## 2. Responsibility Matrix

| Agent          | Role                             | Input                                 | Output                        | Dependencies   | Communication                        |
| -------------- | -------------------------------- | ------------------------------------- | ----------------------------- | -------------- | ------------------------------------ |
| Coordinator    | Manages the overall workflow     | User query                            | Research plan                 | None           | Communicates with all agents         |
| Research Agent | Collects relevant information    | User query and research plan          | Research results              | Coordinator    | Sends results to Analyzer            |
| Analyzer       | Processes and organizes research | Research results                      | Structured analysis           | Research Agent | Sends analysis to Critic             |
| Critic         | Reviews quality and correctness  | Analysis                              | Approval or revision feedback | Analyzer       | Sends feedback to Analyzer or Writer |
| Writer         | Generates final response         | Approved analysis and critic feedback | Final answer                  | Critic         | Sends final answer to Coordinator    |

---

## 3. Detailed Agent Responsibilities

### 3.1 Coordinator Agent

**Role:** Workflow Manager

**Responsibilities:**

* Receive the user's research question.
* Understand the overall task.
* Create a research plan.
* Start the research process.
* Manage the workflow.
* Maintain the shared state.
* Ensure that the correct agent receives the required information.

**Input:**

```text
User Query
```

**Output:**

```text
Research Plan
```

**Dependencies:**

None.

**Communication:**

```text
User → Coordinator
Coordinator → Research Agent
Coordinator ← Writer
Coordinator → User
```

---

### 3.2 Research Agent

**Role:** Information Collector

**Responsibilities:**

* Follow the research plan.
* Identify relevant information.
* Collect important facts.
* Identify examples.
* Identify benefits and challenges.
* Prepare research notes.

**Input:**

```text
User Query
Research Plan
```

**Output:**

```text
Research Results
```

**Dependencies:**

Coordinator.

**Communication:**

```text
Coordinator → Research Agent → Analyzer
```

---

### 3.3 Analyzer Agent

**Role:** Research Analyst

**Responsibilities:**

* Process research results.
* Organize information.
* Identify important findings.
* Remove irrelevant information.
* Compare information.
* Identify patterns.
* Prepare structured analysis.
* Apply Critic feedback when revision is required.

**Input:**

```text
Research Results
Critic Feedback
```

**Output:**

```text
Structured Analysis
```

**Dependencies:**

Research Agent and Critic feedback when available.

**Communication:**

```text
Research Agent → Analyzer → Critic
Critic → Analyzer
```

---

### 3.4 Critic Agent

**Role:** Quality Controller

**Responsibilities:**

* Review the analysis.
* Check relevance.
* Check logical consistency.
* Identify missing information.
* Identify unsupported claims.
* Identify possible weaknesses.
* Approve the analysis or request revision.

**Input:**

```text
User Query
Analysis
```

**Output:**

```text
Approval
OR
Revision Feedback
```

**Dependencies:**

Analyzer.

**Communication:**

```text
Analyzer → Critic

If approved:
Critic → Writer

If rejected:
Critic → Analyzer
```

---

### 3.5 Writer Agent

**Role:** Final Response Generator

**Responsibilities:**

* Use the approved analysis.
* Consider critic feedback.
* Organize the response.
* Create a clear final answer.
* Avoid unnecessary technical details.
* Return only the final response.

**Input:**

```text
User Query
Approved Analysis
Critic Feedback
```

**Output:**

```text
Final Answer
```

**Dependencies:**

Critic approval.

**Communication:**

```text
Critic → Writer → Coordinator → User
```

---

## 4. Communication Matrix

| From           | To             | Information         |
| -------------- | -------------- | ------------------- |
| User           | Coordinator    | Research question   |
| Coordinator    | Research Agent | Research plan       |
| Research Agent | Analyzer       | Research results    |
| Analyzer       | Critic         | Structured analysis |
| Critic         | Analyzer       | Revision feedback   |
| Critic         | Writer         | Approved analysis   |
| Writer         | Coordinator    | Final answer        |
| Coordinator    | User           | Final response      |

---

## 5. Dependency Matrix

| Agent          | Depends On                |
| -------------- | ------------------------- |
| Coordinator    | User                      |
| Research Agent | Coordinator               |
| Analyzer       | Research Agent            |
| Critic         | Analyzer                  |
| Writer         | Critic                    |
| Coordinator    | Writer for final response |

---

## 6. Responsibility Summary

The responsibility distribution can be summarized as:

```text
Coordinator
    ↓
Planning

Research Agent
    ↓
Information Collection

Analyzer
    ↓
Information Processing

Critic
    ↓
Quality Validation

Writer
    ↓
Final Response
```

This separation ensures that every agent has a clear purpose and prevents a single agent from being responsible for the entire research process.
