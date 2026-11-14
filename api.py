
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI(title="Airline Passenger Satisfaction API")

# Load trained ML pipeline
model = joblib.load("models/model_pipeline.pkl")


class PassengerData(BaseModel):
    Type_of_Travel: str
    Class: str
    Customer_Type: str
    Inflight_wifi_service: int
    Online_boarding: int
    Inflight_entertainment: int
    Seat_comfort: int
    Leg_room_service: int


@app.get("/")
def home():
    return {"message": "Airline Satisfaction API is running!"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict")
def predict_satisfaction(data: PassengerData):

    try:
        data_dict = data.model_dump()

        # Convert feature names to original dataset columns
        data_dict = {
            k.replace("_", " "): v
            for k, v in data_dict.items()
        }

        df = pd.DataFrame([data_dict])

        prediction = model.predict(df)

        return {
            "prediction": str(prediction[0])
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
