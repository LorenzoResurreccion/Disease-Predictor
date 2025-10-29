#setup actual api
from flask import Flask, request, jsonify
import pickle
import pandas as pd # Assuming your model expects pandas DataFrames

app = Flask(__name__)

# Load the models once when the application starts
with open('../ML_Models/heart_model.pkl', 'rb') as f:
    heart_model = pickle.load(f)

@app.route('/predict/heart', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    # Assuming input data is a dictionary that can be converted to a DataFrame
    input_df = pd.DataFrame([data])
    prediction = heart_model.predict(input_df)
    probability = heart_model.predict_proba(input_df)
    return jsonify({'prediction': prediction.tolist(), 'probability': probability.tolist()})

if __name__ == '__main__':
    app.run(debug=True)