## Overview

In this task, I explored modern Natural Language Processing (NLP) techniques using Transformer-based models with the Hugging Face library. I worked with pre-trained models for sentiment analysis, question answering, text generation, text summarization, and Named Entity Recognition (NER).

This task helped me understand how Transformer models like BERT and GPT are used in real-world AI applications without training models from scratch.

---

# Learning Objectives

- Understand Transformer architecture
- Learn Transfer Learning in NLP
- Explore Hugging Face Hub
- Understand BERT and GPT models
- Perform Named Entity Recognition (NER)
- Perform Text Summarization
- Use pre-trained NLP models for different tasks

---

# Technologies Used

- Python
- Hugging Face Transformers
- PyTorch
- NLTK
- Jupyter Notebook

---

# Tasks Completed

## 1. Hugging Face Hub Exploration

### Description

Explored the Hugging Face Model Hub and learned how to use pre-trained AI models for different NLP tasks.

### Key Learning

- Hugging Face provides thousands of pre-trained models.
- Models can be used directly through pipelines.
- No need to train models from scratch.

---

# 2. Sentiment Analysis

## Model Used

**distilbert-base-uncased-finetuned-sst-2-english**

### Task

Classified movie reviews and sentences into:

- Positive
- Negative

### Example

Input:


The movie was absolutely amazing and I loved every scene.


Output:


Sentiment: POSITIVE
Confidence: 99.99%


---

# 3. Question Answering Model

## Model Used

**distilbert-base-cased-distilled-squad**

### Task

Answered questions based on provided context.

### Example

Context:


Python was created by Guido van Rossum in 1991.


Question:


Who created Python?


Output:


Guido van Rossum


---

# 4. Text Generation

## Model Used

**GPT-2**

### Task

Generated human-like text using a GPT-based Transformer model.

Example:

Input:


Artificial Intelligence is


Output:


Artificial Intelligence is transforming industries by automating tasks and improving decision making.


---

# 5. Text Summarization

### Task

Converted long paragraphs into shorter summaries while maintaining important information.

Example:

Input:


Long article about Artificial Intelligence applications.


Output:


AI helps machines perform tasks that normally require human intelligence.


---

# 6. Named Entity Recognition (NER)

### Task

Extracted important entities from text.

Example:

Input:


Rahul Rode is studying MCA in Pune and uses Python.


Output:


Person: Rahul Rode
Location: Pune
Technology: Python


---

# Hugging Face Model Exploration

## Selected Model

### Model Name

DistilBERT Sentiment Analysis Model

### Hugging Face Link

https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english

---

## Model Summary

### Purpose

This model is used for sentiment classification of English text.

### Supported Tasks

- Sentiment Analysis
- Text Classification

### Input Format

Plain English text.

Example:


I love this product.


### Output Format

Returns:

- Sentiment label
- Confidence score

Example:


POSITIVE
99.8%


### Real-World Applications

- Movie review analysis
- Customer feedback analysis
- Social media monitoring
- Product review classification
- Chatbot systems

---

# Comparison With Day 9 Model

| Feature | Day 9 NLP Model | Day 10 Transformer Model |
|---|---|---|
| Feature Extraction | TF-IDF | Contextual Embeddings |
| Model Type | Traditional ML | Deep Learning |
| Context Understanding | Limited | High |
| Training Required | Required | Pre-trained |
| Accuracy | Moderate | Higher |
| Tasks Supported | Limited | Multiple NLP Tasks |

---

# Mini Practical Build

## AI Assistant (`ai_assistant.py`)

Created a simple AI assistant using Hugging Face Transformers.

### Features

- Takes user sentence as input
- Predicts sentiment
- Shows confidence score

Example:

Input:


Hugging Face makes NLP easier.


Output:


Sentiment: POSITIVE
Confidence: 99.87%


---

# Project Structure


Day-10/
│
├── sentiment_analysis.py
├── question_answering.py
├── text_generation.py
├── text_summarization.py
├── ner.py
├── ai_assistant.py
└── README.md


---

# Installation

Install required libraries:

```bash
pip install transformers torch sentencepiece