import asyncio
from dataclasses import asdict
from distutils.command.upload import upload
import strawberry
from strawberry.file_uploads import Upload
from typing import Dict, List, Optional
from fastapi import FastAPI
from starlette.responses import StreamingResponse, Response

from strawberry.fastapi import GraphQLRouter
from fastapi.middleware.cors import CORSMiddleware

import requests
import os
import cv2
import psycopg2
import sys


from src.repositories.BookRepo import BookRepo
from src.repositories.SubmissionsRepo import SubmissionRepo
from src.repositories.UserRepo import UserRepo

from src.models.User import User
from src.models.Book import Book
from src.models.Submission import Submission

sys.path.insert(1, "./src/")
from images import make_folders

make_folders()

app = FastAPI()


@app.get("/images/{uuid}/{img_id}")
async def get_image(uuid, img_id):
    """
    uuid is either "mechanims", "values", or unique user ID.
    img_id the image number from the database. i.e from mech-id, values-id, image id in the user id folder
    """
    img = cv2.imread(img_id)
    res, enc_img = cv2.imencode(".jpg", img)
    return Response(enc_img.tobytes(), media_type="image/jpg")


origins = ["http://localhost", "http://localhost:8080", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/submissions")
def read_submissions():
    return [asdict(x) for x in SubmissionRepo().get_submissions()]
