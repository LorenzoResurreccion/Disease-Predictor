#setup actual api
from flask import Flask, request, jsonify
import pandas as pd # Assuming your model expects pandas DataFrames
import joblib, os
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

# list necessary features for for quick check and fill
features = {'Heart':{},
            'Diabetes':{},
            'CKD':{}}

# get paths
ML_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ML_Models')) 
Model_Files = {'Heart': 'heart_model.pkl', 
            'Diabetes':'diabetes_model.pkl',
            'CKD': 'ckd_model.pkl'}

# Load the models once when the application starts
Models = {} 

for label, file in Model_Files.items():
    path = os.path.join(ML_dir, file)
    
    #check if model exists, else assign None
    try:
        Models[label] = joblib.load(path)
    except Exception as e:
        Models[label] = None


"""
Method is used for disease prediction based on features.
Currently Supports: Heart, Diabetes, CKD

disease: specific disease being predicted
data: json provided in request

returns: risk of disease as float, else error if No prediction model is available for disease
"""
def feature_pred(disease, data):
    #check model exists
    model = Models[disease]
    if model is None:
        return f"{disease} Prediction Model Temporarily Unavailable", 503
    
    #check features and fill
    needed_features = features[disease]
    for feature, fill_val in needed_features.items():
        if feature not in data or data[feature] is None:
            data[feature] = fill_val
    
    #predict
    df = pd.DataFrame([data])
    X = df[needed_features]
    risk = model.predict_proba(X)[:,1][0]
    
    return  jsonify({'disease_risk': float(risk)})


"""
Method is used for disease prediction based on Images.
Currently Supports: Skin

disease: specific disease being predicted
data: json provided in request

returns: risk of disease as float, else error if No prediction model is available for disease
"""
def image_pred(disease, data):
    model = Models[disease]

    if model is None:
        return f"{disease} Prediction Model Temporarily Unavailable", 503

    return jsonify({'disease': 'disease name', 'confidence': -1})



@app.route('/predict/<model_name>', methods=['POST'])
def predict(model_name):
    data = request.json

    #call method based on model_name in path
    match model_name:
        case 'heart':
            return feature_pred('Heart', data)
        case  'diabetes':
            return feature_pred('Diabetes', data)
        case 'ckd':
           return feature_pred('CKD', data)
        case 'skin':
            return image_pred('Skin', data)
        case _:
            return "No Matching Model", 400

if __name__ == '__main__':
    app.run(debug=True)