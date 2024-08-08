from fastapi import APIRouter, Request, Body, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
from model.model_loader import model_loader

from controllers.predictions import PREDICTIONS, read_prediction, create_prediction, update_prediction, delete_prediction

router = APIRouter()
templates = Jinja2Templates(directory="templates")

class Prediction(BaseModel):
    id: Optional[str]
    latitude: float
    longitude: float
    lease_term: float
    type: str
    beds: float
    baths: float
    sq_feet: float
    furnishing: str
    smoking: str
    cats: int
    dogs: int
    price_prediction: str

class PredictionFeatures(BaseModel):
    latitude: float
    longitude: float
    lease_term: float
    type: str
    beds: float
    baths: float
    sq_feet: float
    furnishing: str
    smoking: str
    cats: int
    dogs: int

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "predictions": PREDICTIONS})

@router.get("/add-prediction", response_class=HTMLResponse)
async def add_new_prediction(request: Request):
    return templates.TemplateResponse("add-prediction.html", {"request": request})

@router.get("/edit-prediction/{prediction_id}", response_class=HTMLResponse)
async def edit_prediction(request: Request, prediction_id: str):
    prediction = read_prediction(prediction_id)
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return templates.TemplateResponse("edit-prediction.html", {"request": request, "prediction": prediction})

@router.get("/predictions")
async def read_all_predictions():
    print(PREDICTIONS)
    return PREDICTIONS

@router.get("/prediction/{prediction_id}")
async def read_single_prediction(prediction_id: str):
    prediction = read_prediction(prediction_id)
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return prediction

@router.post("/predictions/create_prediction")
async def create_new_prediction(
    latitude: float = Form(...),
    longitude: float = Form(...),
    lease_term: float = Form(...),
    type: str = Form(...),
    beds: float = Form(...),
    baths: float = Form(...),
    sq_feet: float = Form(...),
    furnishing: str = Form(...),
    smoking: str = Form(...),
    cats: int = Form(...),
    dogs: int = Form(...),
    price_prediction: str = Form(...)
):
    new_prediction = {
        "id": str(len(PREDICTIONS) + 1),
        "latitude": latitude,
        "longitude": longitude,
        "lease_term": lease_term,
        "type": type,
        "beds": beds,
        "baths": baths,
        "sq_feet": sq_feet,
        "furnishing": furnishing,
        "smoking": smoking,
        "cats": cats,
        "dogs": dogs,
        "price_prediction": price_prediction,
    }
    create_prediction(new_prediction)
    return RedirectResponse(url="/", status_code=303)

@router.put("/predictions/update_prediction")
async def update_existing_prediction(updated_prediction: dict = Body()):
    update_prediction(updated_prediction)
    return {"message": "Prediction updated successfully"}

@router.delete("/predictions/delete_prediction/{prediction_id}")
async def delete_existing_prediction(prediction_id: str):
    print("Deleting prediction with id:", prediction_id)
    delete_prediction(prediction_id)
    return {"message": "Prediction deleted successfully"}

@router.post("/predict")
async def generate_price_prediction(features: PredictionFeatures):
    features_dict = features.model_dump() 
    print("Features:", features_dict)
    try:
        price = model_loader.predict(features_dict)
        print("Prediction:", price)
        return {"price_prediction": f"${price[0]:.2f}"}  
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
