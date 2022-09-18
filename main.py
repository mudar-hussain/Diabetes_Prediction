# -*- coding: utf-8 -*-
"""Deploying ML Model as Public API.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bbSZt_HfgslPZoAjH_RIfbRX0eiab4dJ

Installing Libraries
"""
"""
!pip install fastapi
!pip install pydantic
!pip install nest-asyncio
!pip install uvicorn
!pip install joblib
!pip install scikit-learn
!pip install requests
!pip install pypi-json
!pip install pyngrok
"""

from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import json
import uvicorn
from pyngrok import ngrok
from fastapi.middleware.cors import CORSMiddleware
import nest_asyncio

"""Instance of FastAPI"""

app = FastAPI()

"""Settings to allow all domain to access our api"""

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']

)

"""Format for input"""

class model_input(BaseModel):
    Pregnancies: int
    Glucose : int
    BloodPressure: int
    SkinThickness: int
    insulin: int
    BMI: float
    DiabetesPedigreeFunction: float
    Age: int

"""Loading the saved Model"""

diabetes_model = joblib.load(r'diabetes_ml_model')

"""API Creation"""

@app.post('/diabetes_prediction')
def diabetes_pred(input_parameters: model_input):
    #print(input_parameters)

    #convert input to dictionary
    input_dict = input_parameters.dict()
    print(input_dict)

    #convert input to dictionary
    #input_data = input_parameters.json()
    #input_dictionary = json.loads(input_data)

    # input_keys = input_dict.keys()
    input_values = [[*input_dict.values()]]

    pred = diabetes_model.predict(input_values)
    if (pred[0] == 1):
        return 'Person is Diabetic'
    else:
        return 'Person is NOT Diabetic'

"""Code Snipper in order to create public url"""

ngrok_tunnel = ngrok.connect(8000)
print('Public URL: ', ngrok_tunnel.public_url)
nest_asyncio.apply()
uvicorn.run(app, port = 8000)

