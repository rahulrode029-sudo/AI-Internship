# Day 13 – Model Deployment using Flask

## Overview

This project demonstrates how to deploy a Machine Learning model using **Flask** by creating a Prediction API. The trained model is serialized using **Joblib/Pickle**, loaded into a Flask application, and exposed through a REST API for real-time predictions. The API is tested using **Postman** with both valid and invalid inputs to verify functionality and error handling.

---

# Learning Objectives

* Understand Model Serialization
* Save and Load Models using Joblib and Pickle
* Build Prediction APIs using Flask
* Implement Error Handling
* Test REST APIs using Postman

---

# Technologies Used

* Python
* Flask
* Scikit-learn
* Pandas
* Joblib
* Pickle
* Postman

---

# Project Structure

```text
Day-13/
│── Model_train.py
│── app.py
│── house_model.pkl
│── House_Data_Price.csv
│── requirements.txt
└── README.md
```

---

# Features

* Train a Machine Learning model.
* Serialize the trained model using Joblib.
* Load the saved model without retraining.
* Create a Flask Prediction API.
* Return predictions in JSON format.
* Handle invalid and missing inputs gracefully.
* Test API endpoints using Postman.

---

# API Endpoint

### **POST /predict**

Predicts the output based on the provided input features.

### Request

```json
{
    "Area": 1800,
    "Bedrooms": 3,
    "Bathrooms": 2
}
```

### Response

```json
{
    "Predicted Price": 5200000.25
}
```

---

# Error Handling

The API validates incoming requests and returns meaningful error messages for:

* Missing required fields
* Invalid data types
* Empty JSON requests
* Negative or zero values
* Internal server errors

Example:

```json
{
    "error": "Area must be greater than 0"
}
```

---

# API Testing

The Prediction API was tested using **Postman** with multiple scenarios, including:

* Valid input values
* Missing fields
* Invalid data types
* Negative values
* Empty JSON requests
* Boundary values

All responses were verified for correctness.

---

# Deliverables

* Flask Prediction API
* Serialized Machine Learning Model
* API Testing Report
* Postman Testing Screenshots
* Edge Case Documentation

---

# How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Train the model

```bash
python Model_train.py
```

This creates:

```text
house_model.pkl
```

### 3. Start the Flask server

```bash
python app.py
```

### 4. Test the API

Use **Postman** to send a **POST** request to:

```text
http://127.0.0.1:5000/predict
```

---

# Key Concepts Learned

* Model Serialization
* Joblib vs Pickle
* Flask REST API Development
* JSON Request & Response
* Prediction API Deployment
* Exception and Error Handling
* API Testing using Postman

---

# Conclusion

This project successfully demonstrates the deployment of a Machine Learning model using Flask. The trained model is serialized, loaded efficiently for prediction, and exposed through a REST API. Comprehensive testing with Postman, including valid, invalid, and edge-case inputs, ensures the API is reliable, robust, and ready for integration into real-world applications.
