from pydantic import BaseModel
from typing import List

class MTMetrics(BaseModel):
    system_length: int
    reference_length: int | None = None
    source_length: int | None = None 
    hyp_segment_qty: int 

class BLEUscore(MTMetrics):
    bleuscore: float
    precisions: list[float]
    brevity_penalty: float

class BARTSegmentScore(BaseModel):
    segment_no: int
    segment_f_score:float
    segment_precision:float
    segment_recall:float

class BARTScore(MTMetrics):
    f_score: float
    precision: float
    recall: float
    segment_scores: list[BARTSegmentScore]

class CKiwiSegmentScore(BaseModel):
    segment_no: int
    segment_score: float 

class COMETKIWIScore(MTMetrics):
    overall_score:float
    segment_scores: list[CKiwiSegmentScore]


class EvaluationResult(BaseModel):
    results: dict[str, BLEUscore | BARTScore | COMETKIWIScore ]


  


