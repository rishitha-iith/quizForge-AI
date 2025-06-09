from pydantic import BaseModel
from typing import List

class Question(BaseModel):
    question: str
    options: List[str]
    correct_index: int  # Store the index (0-3) of the correct answer in the options list