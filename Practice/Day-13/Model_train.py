import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Load Dataset
data = pd.read_csv(r"C:\Users\rahul\OneDrive\Desktop\Ai-Internship\Practice\Day-13\House_Data_Price.csv")

# Features
X = data[["Area", "Bedrooms", "Bathrooms"]]

# Target
y = data["Price"]

# Split Dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train Model
model = LinearRegression()
model.fit(X_train, y_train)

# Save Model
joblib.dump(model, "house_model.pkl")

print("Model saved successfully!")
