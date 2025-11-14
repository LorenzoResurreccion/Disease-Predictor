# Health Predictor using ML

This project will use Flask as the main back-end API. Use multiple Flask APIs to create a microservice architecture while incorporating ML into the system. 

This project will have multiple components: 
1. Jupiter notebooks that are used to analyze the data sets, train the models, evaluate the models, then choose the best prediction model for each condition
2. Flask API for utilizing the created prediction models
3. Seperate Flask Back-end for main app functioning like retrieving/saving data, calling prediction API
4. React.js for front-end interactions

## Data
The data sets were obtained from kaggle: 
- [Heart Disease Dataset](https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset/data)
- [Diabetes Dataset](https://www.kaggle.com/datasets/prosperchuks/health-dataset/data)
- [Chronic Kidney Disease Dataset](https://www.kaggle.com/datasets/abhia1999/chronic-kidney-disease?select=new_model.csv)
- [Skin Disease Dataset](https://www.kaggle.com/datasets/pacificrm/skindiseasedataset/data)


## ML Models
Workflow:
1. Take the data and perform analysis by looking at patterns, correlations, noting down findings on reliability/weaknesses of data, graphing some data using Matplotlib
2. Prep the data by splitting into test and train (and create a copy of scaled/normalized the data)
3. Models were then fit and tested using their defualt hyperparemeters (Except knn where a basic grid search was done for finding the best number of neighbors from 1-15) to evaluate and compare their accuracies
4. If necessary, experiment with some of the models and train further using Grid Search to tune various hyperparameters
5. Select and pickle best model for use

## Prediction API
Work in progress, so far set up a basic idea of how it might look and use the created models. 
Suppsede to work by taking the needed data, making a prediction, and returning the classificatin and its probability. Structure:
1. On start, trys to load all of the models and any necessary data for filling missing features
2. API accepts JSON data to to the endpoint '/prediction/disease_name'
3. API determines uses 'disease_name' to call one of two methods: feature_pred or image_pred depending on what is necessary for risk prediction
4. If no model is avaialble returns '503', else data is prepped then used for prediction 
5. returns classification for images, probabiliy of having disease for features

## App API
Will begin working on it after finished creating/testing the basic functions of the ML API
Planned structure:
1. App API interacts with React front-end
2. received data is stored in database and/or sent to Prediction_api
3. Allow for data to be edited if entered incorrectly
3. returns Prediction API results, past patient records, results of other service interactions

## React.js Front-end
Will beginn working on it after finished creating/testing the basic functions of the App API. Basic functions should allow:
1. retrieval and editing of patient records
2. input of new data and prediction results ot be displayed inntuitively
3. Maybe graphs and trends of user health compared to what is considered optimal

## Possible Improvements
1. Implement scheduled service that would take the new data entries and clean/parse them and add them into the CSVs for model training (like after 10000 new entries or every 2 weeks )
2. Create python files specifically for model training, seperate from the notebooks used for analysis and initial model creation
3. implement scheduled re-training of models (like once a month)
4. implement Prediction api endpoint for reloading models after improved model is made available



