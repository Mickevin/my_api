# Import des librairies uvicorn, pickle, FastAPI, File, UploadFile, BaseModel
from fastapi import FastAPI, File, UploadFile
import uvicorn
import numpy as np
from pydantic import BaseModel
import pickle
import pandas as pd

import mlflow
import os



# Création des tags
tags  = [
    {
        "name": "Hello",
        "description": "Hello World"
    },
    {
        "name": "Predict Model 1",
        "description": "Predict"
    },
    {
        "name": "Upload",
        "description": "Upload : csv file"
    },
    {
        "name": "Root Square",
        "description": "Root Square"
    }
]

# Création de l'application
app = FastAPI(
    title="API de prédiction",
    description="API de prédiction",
    version="1.0.0",
    openapi_tags=tags
)

# Crédentials d'accès à AWS
os.environ['AWS_ACCESS_KEY_ID'] = "AKIA3R62MVALHESATEYJ"
os.environ['AWS_SECRET_ACCESS_KEY'] = "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"
os.environ['ARTIFACT_STORE_URI'] = "s3://isen-mlflow/models/"

mlflow.set_tracking_uri("https://isen-mlflow-fae8e0578f2f.herokuapp.com/")

logged_model = 'runs:/201bd90bf6e747a4af86e0d0f34511af/model'

# Load model as a PyFuncModel.
loaded_model = mlflow.pyfunc.load_model(logged_model)


# Point de terminaison standard
@app.get("/", tags=["Hello", "Root Square"], description="Hello World Test")
def index():
    return {"message": "Hello World!!!"}


# Point de terminaison avec paramètre
@app.get("/hello", tags=["Hello"])
def hello(name: str='World'):
    return {"message": f"Hello {name}"}


# Point de terminaison avec paramètre optionnel dans l'URL
@app.get("/hello/{name}", tags=["Hello"])
def hello(name):
    return {"message": f"Hello {name}"}


# Point de terminaison Post (racine carrée)
@app.post("/root_square", tags=["Root Square"])
def root_square(number: int):
    return {"result": number**0.5}


# Création du modèle de données (age, job, marital, education, default, balance, housing, loan, campaign, pdays, previous, poutcome)
class Credit(BaseModel):
    age: int
    job: int
    marital: int
    education: int
    default: int
    balance: int
    housing: int
    loan: int
    campaign: int
    pdays: int
    previous: int
    poutcome: int

# Point de terminaison : Prédiction
@app.post("/predict", tags=["Predict Model - Mlfow"])
def predict(credit: Credit):

    #with open('model.pkl', 'rb') as f: model = pickle.load(f)
    #predict_value = int(model.predict([list(credit.dict().values())])[0])
    
    predict_value = loaded_model.predict(credit.dict())[0]

    return {"pred" : predict_value}

# Point de terminaison : Prédiction
@app.post("/predict", tags=["Predict Model"])
def predict(credit: Credit):

    with open('model.pkl', 'rb') as f: model = pickle.load(f)
    predict_value = int(model.predict([list(credit.dict().values())])[0])

    return {"pred" : predict_value}


# Point de terminaison qui permet de verser un fichier
@app.post("/uploadfile", tags=["Upload"])
def create_upload_file(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)                                     # Read with pandas
    with open('model.pkl', 'rb') as f: model = pickle.load(f)
    pred = model.predict(df)                                        # Prédiction
    return {"filename": str(pred)}                                  # Retourne le nom du fichier


# Démarage de l'application
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)