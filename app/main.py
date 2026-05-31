from fastapi import FastAPI
from routers.translation_router import translate_router
from routers.evaluation_router import evaluate_router
import logging

import services.translation_service

app = FastAPI()
# logging.basicConfig(filename=r"J:/1_NLP_Data_Engineer/260515_MT_Evaluate/data/mt_log.txt",
#                     level=logging.INFO)
logging.basicConfig(level=logging.INFO)

app.include_router(translate_router)
app.include_router(evaluate_router)