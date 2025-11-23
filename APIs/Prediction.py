#setup actual api
from flask import Flask, request, jsonify
import pandas as pd # Assuming your model expects pandas DataFrames
import joblib, os
from flask_cors import CORS
from ML_Models.globals import Global_Features, Global_Fill_Vals, Global_Model_Files 



def create_app():
    app = Flask(__name__)
    CORS(app) 

    # Path details
    ML_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ML_Models')) 
    
    #assign global dicts to use as initial start values/lists
    Model_Files = Global_Model_Files        #dict of disease: disease_model.pkl
    Features = Global_Features              #dict of disease: [needed_features]
    Fill_vals = Global_Fill_Vals            #dict if feature: value

    # Load the models once when the application starts and whenever method is called
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

                #check features and fill
                needed_features = Features[disease]
                allowed_missing = len(needed_features) * 0.25
                filled = 0
                
                for feature in needed_features:
                    if feature not in data or data[feature] is None:
                        data[feature] = Fill_vals[feature]
                        filled+=1
                
                # if missing > 25% of features return not enough info
                if filled > allowed_missing:
                    Results.append({f'{disease}': 'Not enough features'})
                    continue

                #predict
                df = pd.DataFrame([data])
                X = df[needed_features]
                risk = model.predict_proba(X)[:,1][0]

                #append results
                Results.append({f'{disease}': float(risk)})

            except Exception as e:
                #indicate model doesn't exist
                Results.append( {f'{disease}': "No Existing Model"})

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

    def retrieve_models_list():
        return Model_Files.keys()


    '''
    POST:
        Accepts list of models to update models list and reload the models
        
        JSON should be in the structure:
        {model_name_1 : file_name_1, model_name_2 : file_name_2, ...}

        returns newly assigned Model_Files 

    GET: 
        returns list of models 
    '''
    @app.route('/models', methods=['GET','POST'])
    def models():
        nonlocal Model_Files
        
        if request.method == 'POST':
            #update models list and reload models
            Model_Files = request.get_json()
            load_models()

            return jsonify(Model_Files)
        if request.method == 'GET':
            #return list of available models
            return jsonify(list(Model_Files.keys()))
        
        
        return 'Method Not Allowed', 400


    '''
    POST:
        Accepts list of fill values for disease risk based on features

        JSON should be in the structure:
        {feature_1 : val_1, feature_2 : val_2, ...}

        returns fill values to verify values are different
    GET:
        returns list dict of features:fill_vals
    '''
    @app.route('/fill_values',  methods=['GET', 'POST'])
    def fill_values():
        nonlocal Fill_vals
        if request.method == 'POST':
            Fill_vals = request.get_json()
            return jsonify(Fill_vals)
        if request.method == 'GET':
            return jsonify(Fill_vals)

        return 'Method Not Allowed', 400
       


    '''
    POST:
        Accepts list of fill features for each model

        returns features for verfcation they were updated
    GET:
        returns list of features by model
    '''
    @app.route('/features',  methods=['GET','POST'])
    def features():
        nonlocal Features
        if request.method == 'POST':
            Features = request.get_json()
            return jsonify(Features)
        if request.method == 'GET':
            return Features

        return 'Method Not Allowed', 400
    
    
    
    return app



if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)