# Text Summirization

from transformers import pipeline
summarizer = pipeline("summarization")

text = """
Artificial Intelligence is changing the world.
It helps automate tasks, improves healthcare,
supports education, assists businesses,
and makes everyday life easier through smart applications.
Machine learning and deep learning are important branches of AI.
"""

summary = summarizer(
    text,
    max_length=40,
    min_length=15,
    do_sample=False
)

print(summary[0]["summary_text"])