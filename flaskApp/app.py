from flask import Flask, render_template, request, send_file,send_from_directory
import pandas as pd
from io import BytesIO

app = Flask(__name__, template_folder='templates', static_folder='static')

# Path to the CSV file containing drug response predictions
prediction_file_path = "C:\\Desktop\\CaDRReS-master\\CaDRReS-master\\output\\ccle_all_pred_end.csv"

# Load the predictions DataFrame
predictions_df = pd.read_csv(prediction_file_path, index_col=0)

# Default threshold value
default_threshold = 3

# Prediction function
def predict_drug_response(selected_cell_line, selected_drug, threshold):
    # Check if the threshold is provided, otherwise use the default
    threshold = float(threshold) if threshold is not None else default_threshold

    # Retrieve the prediction from the loaded DataFrame
    prediction = predictions_df.loc[selected_cell_line, selected_drug]

    # Replace this with your logic to interpret the prediction result
    if prediction > threshold:
        sensitivity = 'Sensitive'
    else:
        sensitivity = 'Resistant'

    return sensitivity

# Render Homepage
@app.route('/')
def index():
    cell_lines = predictions_df.index.tolist()
    drugs = predictions_df.columns.tolist()
    return render_template('index.html', cell_lines=cell_lines, drugs=drugs, default_threshold=default_threshold)

# Process Form Data
@app.route('/result', methods=['POST'])
def result():
    selected_cell_line = request.form.get('cell_line')
    selected_drug = request.form.get('drug')

    # Extract the threshold from the form data, set a default if not provided
    threshold = request.form.get('threshold', default=default_threshold, type=float)

    # Call the prediction function with the updated threshold
    sensitivity = predict_drug_response(selected_cell_line, selected_drug, threshold)

    # Get the count of sensitive and resistant cases for the bar chart
    sensitive_cell_lines = predictions_df[predictions_df[selected_drug] > threshold].index.tolist()
    resistant_cell_lines = predictions_df[predictions_df[selected_drug] <= threshold].index.tolist()

    sensitive_count = len(sensitive_cell_lines)
    resistant_count = len(resistant_cell_lines)

    # Save sensitive and resistant cell lines to CSV files
    sensitive_df = pd.DataFrame({'Cell Lines': sensitive_cell_lines})
    resistant_df = pd.DataFrame({'Cell Lines': resistant_cell_lines})

    sensitive_csv = BytesIO()
    resistant_csv = BytesIO()

    sensitive_df.to_csv(sensitive_csv, index=False)
    resistant_df.to_csv(resistant_csv, index=False)

    sensitive_csv.seek(0)
    resistant_csv.seek(0)

    # Return the rendered template with additional variables
    return render_template('result.html', cell_line=selected_cell_line, drug=selected_drug, sensitivity=sensitivity,
                           sensitive_count=sensitive_count, resistant_count=resistant_count,
                           sensitive_cell_lines=sensitive_cell_lines, resistant_cell_lines=resistant_cell_lines)

# Add these routes to your app.py
@app.route('/download_sensitive_csv/<cell_line>/<selected_drug>')
def download_sensitive_csv(cell_line, selected_drug):
    threshold = request.form.get('threshold', default=default_threshold, type=float)
    sensitive_cell_lines = predictions_df[predictions_df[selected_drug] > threshold].index.tolist()
    sensitive_df = pd.DataFrame({'Cell Lines': sensitive_cell_lines})
    sensitive_csv = BytesIO()
    sensitive_df.to_csv(sensitive_csv, index=False)
    sensitive_csv.seek(0)
    return send_file(sensitive_csv, as_attachment=True, download_name=f'{cell_line}_{selected_drug}_sensitive_cell_lines.csv')

@app.route('/download_resistant_csv/<cell_line>/<selected_drug>')
def download_resistant_csv(cell_line, selected_drug):
    threshold = request.form.get('threshold', default=default_threshold, type=float)
    resistant_cell_lines = predictions_df[predictions_df[selected_drug] <= threshold].index.tolist()
    resistant_df = pd.DataFrame({'Cell Lines': resistant_cell_lines})
    resistant_csv = BytesIO()
    resistant_df.to_csv(resistant_csv, index=False)
    resistant_csv.seek(0)
    return send_file(resistant_csv, as_attachment=True, download_name=f'{cell_line}_{selected_drug}_resistant_cell_lines.csv')



path = "C:\\Users\\Asus\\Desktop\\CaDRReS-master\\flaskApp\\static\\animation.json"
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


if __name__ == '__main__':
    app.run(debug=True)
