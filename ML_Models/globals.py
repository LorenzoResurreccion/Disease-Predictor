"""
Can use this file to store dicts, values, or lists that would be used by various files instead 
of re-writing them in each file.

For instance, Prediction.py could use these dicts for starting info then update its internal
values as the updater functions give it new info to work with

"""
Global_Features = {'Heart':['age', 'sex', 'cp', 'trestbps',  'chol', 'fbs', 'restecg',
                'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'],
            'Diabetes':['Age', 'Sex', 'HighChol', 'CholCheck', 'BMI', 'Smoker', 'etc '],
            'CKD':[]}

#stores the values used for filling missing data in predictions or cleaning data
Global_Fill_Vals = {'age': 40, 'sex': 1, 'cp': 0, 'trestbps':60,  'chol':90, 'fbs':0, 'restecg':0,
                'thalach':91, 'exang':0, 'oldpeak':0, 'slope':0, 'ca':0, 'thal':1}

#stores what the model is used to predict and the filename
Global_Model_Files = {'Heart': 'heart_model.pkl', 
                'Diabetes':'diabetes_model.pkl',
                'CKD': 'ckd_model.pkl'}
