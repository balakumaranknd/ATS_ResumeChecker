from pydantic import BaseModel
from typing import List

class ATSResponse(BaseModel):
    match_score: float
    missing_keywords: List[str]