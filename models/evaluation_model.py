from pydantic import BaseModel
from typing import List

class MTMetrics(BaseModel):
    bleuscore: float | None
    precisions: List[float] | None
    brevity_penalty: float | None
    system_length: int | None
    reference_length: int | None