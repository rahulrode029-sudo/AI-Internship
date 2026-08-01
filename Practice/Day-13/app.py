from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load Model
model = joblib.load("house_model.pkl")


@app.route("/")
def home():
    return "House Price Prediction API is Running"


@app.route("/predict", methods=["POST"])
def predict():

    try:

        data = request.get_json()

        if data is None:
            return jsonify({"error": "JSON data is required"}), 400

        required = ["Area", "Bedrooms", "Bathrooms"]

        for column in required:
            if column not in data:
                return jsonify({"error": f"{column} is missing"}), 400

        area = float(data["Area"])
        bedrooms = int(data["Bedrooms"])
        bathrooms = int(data["Bathrooms"])

        if area <= 0:
            return jsonify({"error": "Area must be greater than 0"}), 400

        if bedrooms <= 0:
            return jsonify({"error": "Bedrooms must be greater than 0"}), 400

        if bathrooms <= 0:
            return jsonify({"error": "Bathrooms must be greater than 0"}), 400

        sample = pd.DataFrame({
            "Area": [area],
            "Bedrooms": [bedrooms],
            "Bathrooms": [bathrooms]
        })

        prediction = model.predict(sample)[0]

        return jsonify({
            "Predicted Price": round(float(prediction), 2)
        })

    except ValueError:
        return jsonify({
            "error": "Invalid numeric value"
        }), 400

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)