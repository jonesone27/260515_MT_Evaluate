from fastapi import (
    APIRouter, 
    UploadFile, 
    HTTPException
)

from models.evaluation_model import MTMetrics, COMETKIWIScore
from evaluation_metrics.cometkiwi22 import COMETKIWI
from services.evaluation_service import evaluate_mt

# https://docs.python.org/3/library/logging.html#logging.getLogger
# __name__ = module’s name
import logging
logger = logging.getLogger(__name__)


evaluate_router=APIRouter(
    prefix="/evaluate",
    tags=["evaluation"]
)

@evaluate_router.post("/")
async def evaluate_metrics(hypothesis: UploadFile, reference: UploadFile|None = None, source: UploadFile|None = None):
    reference_list = None
    source_list = None
        
    hyp_text = (await hypothesis.read()).decode("utf-8")
    if hyp_text.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Upload a machine translation document. Additionally upload a reference document and/or the source document for evaluation!"
            ) 
    # Convert to list for alignment of hyp, src and/or ref
    hypothesis_list = hyp_text.splitlines()

    if reference is None and source is None: 
        raise HTTPException(
        status_code=400,
        detail="Upload a reference document and/or the source document to evaluate your machine translation!"
    )

    if reference is not None:
        ref_text = (await reference.read()).decode("utf-8")
        if ref_text.strip() =="":
            raise HTTPException(
                status_code=400,
                detail="Reference document is empty!"
            )
        reference_list = ref_text.splitlines()

       
    if source is not None:
        src_text = (await source.read()).decode("utf-8")
        if src_text.strip()=="":
            raise HTTPException(
                status_code=400,
                detail="Source document is empty!"
            )
        source_list = src_text.splitlines()

    # Evaluate:
    return evaluate_mt(hypo_list=hypothesis_list, 
                       refe_list=reference_list,
                       srce_list=source_list)
    
    
        
  


  
   