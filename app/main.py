from fastapi import FastAPI
from routers.translation_router import translate_router
from routers.evaluation_router import evaluate_router
from prometheus_fastapi_instrumentator import Instrumentator

import logging

import services.translation_service

app = FastAPI()
# logging.basicConfig(filename=r"J:/1_NLP_Data_Engineer/260515_MT_Evaluate/data/mt_log.txt",
#                     level=logging.INFO)
logging.basicConfig(filename="mtrequests.log", 
                    encoding="utf-8", 
                    level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s: %(message)s", 
                    datefmt="%d/%m/%Y %H:%:M%:%S")

app.include_router(translate_router)
app.include_router(evaluate_router)

# See https://pypi.org/project/prometheus-fastapi-instrumentator/
Instrumentator().instrument(app).expose(app)