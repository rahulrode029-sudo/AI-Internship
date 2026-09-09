# Hugging Face Sentiment Analysis

from transformers import pipeline

sentiment = pipeline("sentiment-analysis")

reviews = [
    "The movie was absolutely amazing and I loved every scene.",
    "The acting was terrible and the story was boring.",
    "The movie was okay."
]

for review in reviews:
    result = sentiment(review)

    print("=" * 50)
    print("Review :", review)
    print("Prediction :", result[0]["label"])
    print("Confidence :", round(result[0]["score"] * 100, 2), "%")
    
   