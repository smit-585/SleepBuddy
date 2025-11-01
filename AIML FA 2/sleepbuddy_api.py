from flask import Flask, request, jsonify
from flask_cors import CORS  # import CORS
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173", "http://127.0.0.1:5173"])

# Load model and preprocessors
model = joblib.load("sleep_quality_model.pkl")
scaler = joblib.load("scaler.pkl")
label_encoders = joblib.load("label_encoders.pkl")

@app.route("/api/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        
        # Handle "None" sleep disorder by converting to NaN
        if data.get("Sleep Disorder") == "None":
            data["Sleep Disorder"] = np.nan

        # Convert input to DataFrame
        X = pd.DataFrame([data])

        # Encode categorical columns
        for col, le in label_encoders.items():
            if col in X.columns:
                # Handle missing values properly
                X[col] = X[col].fillna(le.classes_[0])
                # Handle unknown categories
                X[col] = X[col].apply(lambda x: x if x in le.classes_ else le.classes_[0])
                X[col] = le.transform(X[col])

        # Scale numerical features
        X_scaled = scaler.transform(X)

        # Make prediction
        prediction = model.predict(X_scaled)[0]
        probs = model.predict_proba(X_scaled)[0]

        return jsonify({
            "prediction": prediction,
            "probabilities": dict(zip(model.classes_, probs.round(3)))
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
