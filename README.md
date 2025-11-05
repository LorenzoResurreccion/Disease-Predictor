# Health Predictor using ML

This project will use Springboot as the main back-end API. This is because I wanted to simulate a seting where there already existed a health system where people entered various health data and had health data stored, and they wanted to begin incorporating ML into their systems. 

This project will have multiple components: 
1. Jupiter notebooks that are used to analyze the data sets, train the models, evaluate the models, then choose the best prediction model for each condition
2. Flask API for utilizing the. created models
3. Springboot back-end that will act as our main API
4. React.js front-end

## Data
The data sets were obtained from kaggle: 
-[Heart Disease Dataset](https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset/data)
-[Diabetes Dataset](https://www.kaggle.com/datasets/prosperchuks/health-dataset/data)
-[Chronic Kidney Disease Dataset](https://www.kaggle.com/datasets/abhia1999/chronic-kidney-disease?select=new_model.csv)
-[Skin Disease Dataset](https://www.kaggle.com/datasets/pacificrm/skindiseasedataset/data)


## ML Models
Workflow:
1. Take the data and perform analysis by looking at patterns, correlations, noting down findings on reliability/weaknesses of data, graphing some data using Matplotlib
2. Prep the data by splitting into test and train (and create a copy of scaled/normalized the data)
3. Models were then fit and tested using their defualt hyperparemeters (Except knn where a basic grid search was done for finding the best number of neighbors from 1-15) to evaluate and compare their accuracies
4. If necessary, experiment with some of the models and train further using Grid Search to tune various hyperparameters
5. Select and pickle best model for use

## Flask API
Work in progress, so far set up a basic idea of how it might look and use the created models. 
Suppsede to work by taking the needed data, making a prediction, and returning the classificatin and its probability.  

## Springboot API
will begin working on it after finished creating/testing the basic functions of the Flask API

## React.js Front-end
Will beginn working on it after finished creating/testing the basic functions of the Spring API


