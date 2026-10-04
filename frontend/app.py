import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

# Set the title of the Streamlit app
st.title("Superkart Sales Prediction")

# Section for online prediction
st.subheader("Online Prediction")

# Collect user input for Superkart features
product_weight = st.number_input("Product Weight", min_value=4.0, max_value=22.0, value=12.65, step=0.1)
product_sugar_content = st.selectbox("Product Sugar Content", ['Low Sugar', 'Regular', 'No Sugar'], index=0)
product_allocated_area = st.number_input("Product Allocated Area", min_value=0.004, max_value=0.298, value=0.068, format="%.3f")
product_mrp = st.number_input("Product MRP", min_value=31.0, max_value=266.0, value=147.0, step=0.1)
store_size = st.selectbox("Store Size", ['Medium', 'High', 'Small'], index=0)
store_location_city_type = st.selectbox("Store Location City Type", ['Tier 2', 'Tier 1', 'Tier 3'], index=0)
store_type = st.selectbox("Store Type", ['Supermarket Type2', 'Departmental Store', 'Supermarket Type1', 'Food Mart'], index=0)
product_id_char = st.selectbox("Product ID Character (e.g., FD, NC, DR)", ['FD', 'NC', 'DR'], index=0)
store_age_years = st.number_input("Store Age (Years)", min_value=15, max_value=40, value=25)
product_type_category = st.selectbox("Product Type Category (e.g., FD, NC, DR)", ['FD', 'NC', 'DR'], index=0)

# Convert user input into a DataFrame
input_data = pd.DataFrame([{
    'Product_Weight': product_weight,
    'Product_Sugar_Content': product_sugar_content,
    'Product_Allocated_Area': product_allocated_area,
    'Product_MRP': product_mrp,
    'Store_Size': store_size,
    'Store_Location_City_Type': store_location_city_type,
    'Store_Type': store_type,
    'Product_Id_char': product_id_char,
    'Store_Age_Years': store_age_years,
    'Product_Type_Category': product_type_category
}])

# Make prediction when the "Predict" button is clicked
if st.button("Predict", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/superkartsale", json=input_data.to_dict(orient='records')[0])  # Send data to Flask API
    if response.status_code == 200:
        prediction = response.json()['Predicted sales (in dollars)']
        st.success(f"Predicted Sales (in dollars): {prediction:.2f}")
    else:
        st.error(f"Unable to connect to the prediction API. Error: {response.status_code} - {response.text}")

# Section for batch prediction
st.subheader("Batch Prediction")

# Allow users to upload a CSV file for batch prediction
uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

# Make batch prediction when the "Predict Batch" button is clicked
if uploaded_file is not None:
    if st.button("Predict Batch", type="primary", key="predict_batch_button"):
        # Ensure the uploaded file is processed correctly for batch prediction
        files = {'file': uploaded_file.getvalue()}
        response = requests.post(f"{BACKEND_URL}/v1/superkartsalebatch", files=files)  # Send file to Flask API
        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch predictions completed!")
            st.write(predictions)  # Display the predictions
        else:
            st.error(f"Unable to connect to the prediction API. Error: {response.status_code} - {response.text}")
