from typing import List
import datetime
from dataclasses import dataclass


@dataclass
class Question:
    id: int
    content: str
    response: int


@dataclass
class Submission:
    id: int
    score: int
    questions: List[Question]
    submitted_at: datetime.datetime
