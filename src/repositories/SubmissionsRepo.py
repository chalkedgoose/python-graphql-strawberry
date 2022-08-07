from typing import Dict, List
from urllib import response
from src.models.Submission import Question, Submission
import uuid
import datetime


class SubmissionRepo:
    #each_submission = Submission(response, question_content, id, score, submitted_at)

    submission_db = [
        Submission(
            id=1,
            score=69,
            questions=[
                Question(
                    id=1,
                    content="YEEET",
                    response=0
                ),
                Question(
                    id=1,
                    content="CUSSSSY",
                    response=3
                )
            ],
            submitted_at=datetime.datetime.now()
        )

    ]

    def get_submissions(self) -> List[Submission]:
        return self.submission_db
