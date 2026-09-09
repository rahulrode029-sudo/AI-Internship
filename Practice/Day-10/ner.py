# named Entity Recognition

from transformers import pipeline

ner = pipeline(
    "ner",
    grouped_entities=True
)

sentence = "Rahul Rode is studying MCA in Pune and uses Python."

result = ner(sentence)

for entity in result:
    print(entity)