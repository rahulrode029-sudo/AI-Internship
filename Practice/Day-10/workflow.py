from transformers import pipeline

# Sentiment
sentiment = pipeline("sentiment-analysis")

print("sentiment is completed\n")

# QA
qa = pipeline("question-answering")

print("QA is completed\n")

# Text Generation
generator = pipeline("text-generation", model="gpt2")

print("generator is completed \n")

# Summarization
#summarizer = pipeline("summarization")

from transformers import pipeline

summarizer = pipeline(
    "summarization",
    model="t5-small"
)


print("summerizer is completed\n")

# NER
ner = pipeline("ner", grouped_entities=True)

print("\nAll Hugging Face models loaded successfully!")