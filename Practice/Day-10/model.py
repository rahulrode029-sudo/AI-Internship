# exploration of Hugging face model

model_name = "distilbert-base-uncased-finetuned-sst-2-english"

print("Model Name :", model_name)

print("""
Purpose:
Sentiment Analysis

Supported Tasks:
- Positive/Negative Classification

Input:
English Text

Output:
Label + Confidence Score

Applications:
- Movie Reviews
- Product Reviews
- Social Media Analysis
- Customer Feedback
""")

from transformers import pipeline

classifier = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

result = classifier("The movie was amazing!")
print(result)