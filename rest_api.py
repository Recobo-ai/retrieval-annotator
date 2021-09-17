import pandas as pd
import os
from annotation_mongo import MongoAnnotation
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


annotator_name = os.environ["ANNOTATOR_NAME"]
annotator_file_name = os.environ["DATA_FILE_PATH"]


## mongo credentials from environment variables
credentials = {
    "mongo_username": os.environ["MONGO_USERNAME"],
    "mongo_password": os.environ["MONGO_PASSWORD"],
}

mongo_db_config = {
    "mongo_connect_url": "mongodb+srv://{}:{}@cluster0.lhdpw.mongodb.net/{}?retryWrites=true&w=majority",
    "mongo_db": "chemical_domain_annotations",
    "mongo_collection": "chemical_domain_annotations",
}
mongo_db_config_questions = {
    "mongo_connect_url": "mongodb+srv://{}:{}@cluster0.lhdpw.mongodb.net/{}?retryWrites=true&w=majority",
    "mongo_db": "chemical_domain_annotations",
    "mongo_collection": "questions",
}
mongo_annotation_manager = MongoAnnotation(credentials, mongo_db_config)
mongo_questions_manager = MongoAnnotation(credentials, mongo_db_config_questions)

# Number of entries per screen
N = 2

min_page_num = 0


app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/annotation/page_number")
async def get_page_number(annotator_name: str):
    annotator_page_num = mongo_annotation_manager.get_page_number(
        annotator_name=annotator_name, annotator="annotator", col="page_number"
    )
    annotator_total_pages = (
        mongo_questions_manager.get_page_number(
            annotator_name=annotator_name, annotator="annotator_name", col="row_num"
        )
        + 1
    ) // 2
    response = {"page_number": annotator_page_num, "total_pages": annotator_total_pages}
    return response
