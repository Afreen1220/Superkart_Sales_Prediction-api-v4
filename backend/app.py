# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application
superkart_sales_predictor_api = Flask("Superkart Sales Predictor")

# Load the trained machine learning model
model = joblib.load("superkart_model_v1_0.joblib")

# Define a route for the home page (GET request)
@superkart_sales_predictor_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome tp superkart sale  Prediction API!"

# Define an endpoint for single property prediction (POST request)
@superkart_sales_predictor_api.post('/v1/superkartsale')
def predict_superkart_sales():
    """
    This function handles POST requests to the '/v1/superkartsale' endpoint.
    It expects a JSON payload containing property details and returns
    the predicted rental price as a JSON response.
    """
    # Get the JSON data from the request body
    property_data = request.get_json()

    # Extract relevant features from the JSON data
    sample = {
        'Product_Weight': property_data['Product_Weight'],
        'Product_Sugar_Content': property_data['Product_Sugar_Content'],
        'Product_Allocated_Area': property_data['Product_Allocated_Area'],
        'Product_MRP': property_data['Product_MRP'],
        'Store_Size': property_data['Store_Size'],
        'Store_Location_City_Type': property_data['Store_Location_City_Type'],
        'Store_Type': property_data['Store_Type'],
        'Product_Id_char': property_data['Product_Id_char'],
        'Store_Age_Years': property_data['Store_Age_Years'],
        'Product_Type_Category': property_data['Product_Type_Category'],
    }

    # Convert the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])

    predicted_superkart_sales = model.predict(input_data)[0]


    # When we send this value directly within a JSON response, Flask's jsonify function encounters a datatype error

    # Return the actual price
    return jsonify({'Predicted sales (in dollars)': predicted_superkart_sales})


# Define an endpoint for batch prediction (POST request)
@superkart_sales_predictor_api.post('/v1/superkartsalebatch')
def predict_superkart_sales_batch():
    """
    This function handles POST requests to the '/v1/superkartsalebatch' endpoint.
    It expects a CSV file containing property details for multiple properties
    and returns the predicted rental prices as a dictionary in the JSON response.
    """
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the CSV file into a Pandas DataFrame
    input_data = pd.read_csv(file) # Read directly from the file object

    # Make predictions for all properties in the DataFrame
    predicted_superkart_sales = model.predict(input_data).tolist()

    # Create a dictionary of predictions with product IDs as keys
    # Assuming 'Product_Id' is a column in the batch data, which needs to be available in the uploaded file.
    # For this example, we'll use a simple index if 'Product_Id' is not present in the batch_data.csv
    if 'Product_Id' in input_data.columns:
      product_ids = input_data['Product_Id'].tolist()
    else:
      product_ids = [f'product_{i}' for i in range(len(input_data))]

    output_dict = dict(zip(product_ids, predicted_superkart_sales))

    # Return the predictions dictionary as a JSON response
    return jsonify(output_dict)

# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    superkart_sales_predictor_api.run(debug=True)
