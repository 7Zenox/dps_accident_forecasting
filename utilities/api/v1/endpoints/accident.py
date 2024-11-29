import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import asyncio
from utilities.helpers import response
from utilities.helpers.accident.accident_pred import main

router = APIRouter()

class PredictionRequest(BaseModel):
    year: int
    month: int

@router.post("/")
async def get_accident_prediction(request: PredictionRequest):
    year = request.year
    month = request.month

    try:
        prediction_result = await asyncio.to_thread(main, year, month)
        return response.create_response(
            success=True, data=prediction_result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))