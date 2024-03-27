# Drug Response Predictor

## Overview
Drug Response Predictor is a web application built using Flask, a Python web framework, and HTML/CSS/JavaScript for the front-end. It allows users to predict the response of cancer cell lines to different drugs based on provided data.

## Key Features
- **Homepage:** Users can select a specific cancer cell line and a drug from dropdown menus.
- **Result Page:** Predicted response (sensitive or resistant) for the chosen combination is displayed.
- **Dynamic Dropdowns:** Dropdown menus dynamically update to show the selected items.

## Technologies Used
- Flask
- HTML/CSS/JavaScript
- Pandas
- Plotly Express
- Numpy
- Scipy
- Argparse

## Installation
1. CaDRReS_model.pickle is a file containing an existing model
drug_response_ic50_test.csv contains an empty matrix where rows are cell lines and columns are features
cell_line_features.csv contains a feature matrix where rows are the cell lines to be analyzed and columns are features. The features have to match with the features used for training the model.

2. Install the required dependencies:
- Pandas
- Plotly Express
- Numpy
- Scipy
- Argparse

## Usage
1. Navigate to the project directory.
2. Run the Flask application:
python app.py
3. Access the application through the provided URL in the browser.

## Future Improvements
- Integration with machine learning models for more accurate predictions.
- Expansion of the dataset to include more cell lines and drugs.
- Enhancement of the user interface with additional features and visualizations.

