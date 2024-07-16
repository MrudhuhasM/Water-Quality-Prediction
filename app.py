import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from waterquality.predict import make_prediction

load_dotenv()

app = FastAPI()

# CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class WaterQuality(BaseModel):
    aluminium: float
    ammonia: float
    arsenic: float
    barium: float
    cadmium: float
    chloramine: float
    chromium: float
    copper: float
    flouride: float
    bacteria: float
    viruses: float
    lead: float
    nitrates: float
    nitrites: float
    mercury: float
    perchlorate: float
    radium: float
    selenium: float
    silver: float
    uranium: float


@app.get("/")
def read_root():
    return {"welcome": "Welcome to the Water Quality Prediction API"}


@app.post("/predict/")
def predict(data: WaterQuality):
    """
    Make a prediction using a pre-trained model.

    Args:
        data (dict): A dictionary containing the data to be used for prediction.
    """
    data = data.model_dump()
    prediction = make_prediction(data)
    return {"prediction": prediction}


if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    port = os.getenv("PORT", 8000)
    uvicorn.run(app, host=host, port=port)
