from transformers import pipeline


# Load Hugging Face Sentiment Analysis Model
sentiment_model = pipeline(
    "sentiment-analysis",
    model="distilbert/distilbert-base-uncased-finetuned-sst-2-english"
)


print("AI Sentiment Assistant")


while True:

    # Taking input from user
    sentence = input("\nEnter a sentence (type 'exit' to stop): ")


    # Exit condition
    if sentence.lower() == "exit":
        print("\nAI Assistant stopped.")
        break


    # Predict sentiment
    result = sentiment_model(sentence)


    # Extract output
    label = result[0]["label"]
    confidence = result[0]["score"]


    # Display result
    print("\nPrediction Result")
    print("-" * 30)
    print("Sentence :", sentence)
    print("Sentiment:", label)
    print("Confidence:", round(confidence * 100, 2), "%")