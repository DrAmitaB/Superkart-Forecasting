
# Import Streamlit for creating the web interface
import streamlit as st

# Import requests for communicating with the Flask API
import requests

# Import pandas for handling batch CSV data
import pandas as pd


# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------

# Configure the Streamlit page
st.set_page_config(
    page_title="SuperKart Sales Prediction",
    page_icon="📊",
    layout="wide"
)


# ---------------------------------------------------------
# Application Title
# ---------------------------------------------------------

# Display the application title
st.title("SuperKart Sales Prediction")

# Display a short description
st.write(
    "Predict product-store sales using the trained SuperKart "
    "machine learning model."
)


# ---------------------------------------------------------
# Backend API Configuration
# ---------------------------------------------------------

# Define the backend URL inside the Docker network
# Use the Codespace host because the frontend runs with host networking
BACKEND_URL = "http://127.0.0.1:7860"

# ---------------------------------------------------------
# Online Prediction
# ---------------------------------------------------------

# Create a section for single-record prediction
st.header("Online Prediction")

# Create two columns for numerical inputs
col1, col2 = st.columns(2)

with col1:

    # Accept product weight
    product_weight = st.number_input(
        "Product Weight",
        min_value=0.0,
        value=12.0
    )

    # Accept product allocated area
    product_allocated_area = st.number_input(
        "Product Allocated Area",
        min_value=0.0,
        value=10.0
    )

    # Accept product MRP
    product_mrp = st.number_input(
        "Product MRP",
        min_value=0.0,
        value=100.0
    )

    # Accept store age
    store_age = st.number_input(
        "Store Age",
        min_value=0,
        value=10
    )


with col2:

    # Select product sugar content
    product_sugar_content = st.selectbox(
        "Product Sugar Content",
        ["Low Sugar", "Regular", "No Sugar"]
    )

    # Select product type
    product_type = st.selectbox(
        "Product Type",
        [
            "Baking Goods",
            "Breads",
            "Breakfast",
            "Canned",
            "Dairy",
            "Frozen Foods",
            "Fruits and Vegetables",
            "Hard Drinks",
            "Health and Hygiene",
            "Household",
            "Meat",
            "Others",
            "Seafood",
            "Snack Foods",
            "Soft Drinks",
            "Starchy Foods"
        ]
    )

    # Select store ID
    store_id = st.selectbox(
        "Store ID",
        ["OUT001", "OUT002", "OUT003", "OUT004"]
    )

    # Select store size
    store_size = st.selectbox(
        "Store Size",
        ["Small", "Medium", "High"]
    )

    # Select city type
    store_location_city_type = st.selectbox(
        "Store Location City Type",
        ["Tier 1", "Tier 2", "Tier 3"]
    )

    # Select store type
    store_type = st.selectbox(
        "Store Type",
        [
            "Departmental Store",
            "Supermarket Type1",
            "Supermarket Type2",
            "Food Mart"
        ]
    )


# Create the prediction button
if st.button("Predict Sales"):

    # Create the input dictionary using the model features
    input_data = {
        "Product_Weight": product_weight,
        "Product_Sugar_Content": product_sugar_content,
        "Product_Allocated_Area": product_allocated_area,
        "Product_Type": product_type,
        "Product_MRP": product_mrp,
        "Store_Id": store_id,
        "Store_Size": store_size,
        "Store_Location_City_Type": store_location_city_type,
        "Store_Type": store_type,
        "Store_Age": store_age
    }

    # Send the input data to the Flask backend
    response = requests.post(
        f"{BACKEND_URL}/v1/superkart",
        json=input_data
    )

    # Check whether the request was successful
    if response.status_code == 200:

        # Extract the prediction from the response
        result = response.json()

        # Display the predicted sales
        st.success(
            f"Predicted Product-Store Sales: "
            f"{result['predicted_sales']:,.2f}"
        )

    else:

        # Display an error message if prediction fails
        st.error(
            f"Prediction failed. Status code: "
            f"{response.status_code}"
        )


# ---------------------------------------------------------
# Batch Prediction
# ---------------------------------------------------------

# Create a section for batch prediction
st.header("Batch Prediction")

# Allow the user to upload a CSV file
uploaded_file = st.file_uploader(
    "Upload a CSV file",
    type=["csv"]
)


# Check whether a file has been uploaded
if uploaded_file is not None:

    # Read the uploaded CSV file
    batch_data = pd.read_csv(uploaded_file)

    # Display the uploaded data
    st.write("Uploaded Data")
    st.dataframe(batch_data)

    # Create the batch prediction button
    if st.button("Predict Batch"):

        # Reset the file pointer before sending the file
        uploaded_file.seek(0)

        # Prepare the CSV file for the API request
        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "text/csv"
            )
        }

        # Send the CSV file to the batch prediction endpoint
        response = requests.post(
            f"{BACKEND_URL}/v1/superkartbatch",
            files=files
        )

        # Check whether the request was successful
        if response.status_code == 200:

            # Convert the response into a DataFrame
            predictions = pd.DataFrame(
                response.json()
            )

            # Display a success message
            st.success(
                "Batch predictions completed successfully!"
            )

            # Display the prediction results
            st.dataframe(predictions)

        else:

            # Display an error message
            st.error(
                f"Batch prediction failed. Status code: "
                f"{response.status_code}"
            )
