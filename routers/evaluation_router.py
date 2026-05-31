from fastapi import (
    APIRouter, 
    UploadFile, 
    HTTPException
)

from models.evaluation_model import MTMetrics

from services.evaluation_service import evaluate_mt

evaluate_router=APIRouter(
    prefix="/evaluate",
    tags=["evaluation"]
)

@evaluate_router.post("/{metric}", response_model=MTMetrics)
async def evaluate_metrics(metric: str, hypothesis: UploadFile, reference: UploadFile):
    hyp_bytes = await hypothesis.read()
    ref_bytes = await reference.read()


    mt_eval = evaluate_mt(metric=metric, mt_hyp=hyp_bytes, mt_ref=ref_bytes)
    return mt_eval

   