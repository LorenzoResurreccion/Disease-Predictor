#setup actual api
from flask import Flask, request, jsonify
import pandas as pd # Assuming your model expects pandas DataFrames
import joblib, os
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

# list necessary features for for quick check and fill (median/mean/mode can be used)
# maybe implement fill using user's health history and use general fill val if still missing
Features = {'Heart':['age', 'sex', 'cp', 'trestbps',  'chol', 'fbs', 'restecg',
                    'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'],
            'Diabetes':['Age, Sex, HighChol, CholCheck, BMI, Smoker,  '],
            'CKD':[]}

Fill_vals = {'age': 40, 'sex': 1, 'cp': 0, 'trestbps':60,  'chol':90, 'fbs':0, 'restecg':0,
                    'thalach':91, 'exang':0, 'oldpeak':0, 'slope':0, 'ca':0, 'thal':1}

# Path details
ML_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ML_Models')) 
Model_Files = {'Heart': 'heart_model.pkl', 
            'Diabetes':'diabetes_model.pkl',
            'CKD': 'ckd_model.pkl'}

# Load the models once when the application starts
Models = {} 
def load_models(): 
    for label, file in Model_Files.items():
        path = os.path.join(ML_dir, file)
        
        #check if model exists, else assign None
        try:
            model = joblib.load(path)
            Models[label] = model
            print(f'{label} model loaded')
        except Exception as e:
            Models[label] = None
            print(f'{label} model not found')

load_models()


"""
Method is used for disease prediction based on features.
Currently Supports: Heart, Diabetes, CKD

disease: specific disease being predicted
data: json provided in request

returns: risk of disease as float, else error if No prediction model is available for disease
"""
def feature_pred(diseases, data):
    Results = []
    
    # iterate through models
    for disease in diseases: 
       
        try:
            #check model exists
            model = Models[disease]  
            if model is None:
                #model exists but is down
                Results.append( {f'{disease}': "Prediction Model Temporarily Unavailable"})
    
            print('model selected')
            #check features and fill
            needed_features = Features[disease]
            for feature in needed_features:
                if feature not in data or data[feature] is None:
                    data[feature] = Fill_vals[feature]
            print('features checked')
            
            #predict
            df = pd.DataFrame([data])
            X = df[needed_features]
            risk = model.predict_proba(X)[:,1][0]
            print('prediction made')

            #append results
            Results.append({f'{disease}': float(risk)})

        except Exception as e:
            #indicate model doesn't exist
            Results.append( {f'{disease}': "No Exising Model"})

    return jsonify(Results)


"""
Method is used for disease prediction based on Images.
Currently Supports: Skin

disease: specific disease being predicted
data: json provided in request

returns: disease classification/confidence, else error if No prediction model is available for disease
"""
def image_pred(disease, data):
    model = Models[disease]

    if model is None:
        return f"{disease} Prediction Model Temporarily Unavailable", 503

    return jsonify({'disease': 'disease name', 'confidence': -1})



@app.route('/prediction/<type>', methods=['POST'])
def prediction(type):
    req = request.json
    diseases = req.get('diseases')
    data = req.get('data')

    #call method based on model_name in path
    match type:
        case 'feature':
            return feature_pred(diseases, data)
        case 'image':
            return image_pred(diseases, data)
        case _:
            return "No Matching Models", 400
        
'''
Accepts list of models to update models list and reload the models

JSON should be in the structure:
{model_name_1 : file_name_1, model_name_2 : file_name_2, ...}

returns 200 indicating models were successfuly loaded and list updated
'''
@app.route('/models', methods=['POST'])
def models():
    data = request.json
    Model_Files = data.get('models')
    load_models()

    return jsonify(Model_Files)


'''
Accepts list of fill values for disease risk based on features

JSON should be in the structure:
{feature_1 : val_1, feature_2 : val_2, ...}

returns 200 indicating fill values were successfuly updated
'''
@app.route('/fill_values',  methods=['POST'])
def fill_values():
    data = request.json
    fill_vals = data.get('values')

    return "Fill Values updated", 200


'''
Accepts list of fill features for each model

returns 200 indicating features were successfuly updated
'''
@app.route('/features',  methods=['POST'])
def features():
    data = request.json
    features = data.get('features')

    return "Features updated", 200



if __name__ == '__main__':
    app.run(debug=True)