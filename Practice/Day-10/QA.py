#Que-Ans Model
from transformers import pipeline

qa = pipeline(
    "question-answering",
    model="deepset/tinyroberta-squad2"
)

context = "Python was created by Guido van Rossum."

result = qa(
    question="Who created Python?",
    context=context
)

print(result)