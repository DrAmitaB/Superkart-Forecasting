
from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load the trained SuperKart model
model = joblib.load("model.pkl")


@app.route("/v1/superkart", methods=["POST"])
def predict():
    # Get JSON input from the request
    data = request.get_json()

    # Convert the input into a DataFrame
    input_data = pd.DataFrame([data])

    # Generate the sales prediction
    prediction = model.predict(input_data)

    # Return the prediction as JSON
    return jsonify({
        "predicted_sales": float(prediction[0])
    })


@app.route("/v1/superkartbatch", methods=["POST"])
def predict_batch():
    # Check whether a CSV file was uploaded
    if "file" not in request.files:
        return jsonify({"error": "No CSV file uploaded"}), 400

    # Read the uploaded CSV file
    file = request.files["file"]
    batch_data = pd.read_csv(file)

    # Create a copy so that the original uploaded data is preserved
    batch_df = batch_data.copy()

    # Create Store_Age using the Store_Age_Years column
    batch_df["Store_Age"] = batch_df["Store_Age_Years"]

    # Rename Product_Type_Category to Product_Type
    # so that it matches the feature used during model training
    batch_df["Product_Type"] = batch_df["Product_Type_Category"]

    # The raw batch CSV does not contain Store_Id.
    # Use OUT004 as the Store_Id for these batch records,
    # matching the batch prediction preparation used in the notebook.
    batch_df["Store_Id"] = "OUT004"

    # Select the features required by the trained model
    batch_features = batch_df[
        [
            "Product_Weight",
            "Product_Sugar_Content",
            "Product_Allocated_Area",
            "Product_MRP",
            "Store_Size",
            "Store_Location_City_Type",
            "Store_Type",
            "Store_Age",
            "Product_Type",
            "Store_Id"
        ]
    ]

    # Generate sales predictions for all uploaded records
    predictions = model.predict(batch_features)

    # Add predictions to the original batch data
    batch_data["Predicted_Product_Store_Sales_Total"] = predictions

    # Return the batch data with predictions as JSON
    return jsonify(batch_data.to_dict(orient="records"))


if __name__ == "__main__":
    # Run Flask on all network interfaces
    app.run(
        host="0.0.0.0",
        port=7860,
        debug=False
    )