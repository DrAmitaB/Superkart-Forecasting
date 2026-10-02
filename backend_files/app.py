
# Import Flask functions for creating the REST API
from flask import Flask, request, jsonify

# Import joblib to load the trained machine learning model
import joblib

# Import pandas to process incoming tabular data
import pandas as pd

# Create the Flask application
app = Flask(__name__)

# Load the saved SuperKart model
model = joblib.load("model.pkl")


# ---------------------------------------------------------
# Online Prediction Endpoint
# ---------------------------------------------------------

# Define the endpoint for predicting sales for one record
@app.route("/v1/superkart", methods=["POST"])
def predict():

    # Get the JSON data sent by the client
    data = request.get_json()

    # Convert the JSON record into a pandas DataFrame
    input_data = pd.DataFrame([data])

    # Generate the sales prediction
    prediction = model.predict(input_data)

    # Return the prediction as a JSON response
    return jsonify({
        "predicted_sales": float(prediction[0])
    })


# ---------------------------------------------------------
# Batch Prediction Endpoint
# ---------------------------------------------------------

# Define the endpoint for batch predictions using a CSV file
@app.route("/v1/superkartbatch", methods=["POST"])
def predict_batch():

    # Check whether a file was included in the request
    if "file" not in request.files:
        return jsonify({
            "error": "No CSV file uploaded"
        }), 400

    # Read the uploaded CSV file
    file = request.files["file"]
    input_data = pd.read_csv(file)

    # Generate predictions for all records
    predictions = model.predict(input_data)

    # Add predictions to the input DataFrame
    input_data["Predicted_Product_Store_Sales_Total"] = predictions

    # Return the batch predictions as JSON
    return jsonify(
        input_data.to_dict(orient="records")
    )


# ---------------------------------------------------------
# Start Flask Application
# ---------------------------------------------------------

# Start the Flask application when this file is executed
if __name__ == "__main__":

    # Listen on all available network interfaces
    app.run(
        host="0.0.0.0",

        # Use port 7860 as required for the deployment
        port=7860,

        # Disable debug mode for deployment
        debug=False
    )
