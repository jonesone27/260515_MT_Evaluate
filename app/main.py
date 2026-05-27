from fastapi import FastAPI
from routers.translation_router import translate_router
from routers.evaluation_router import evaluate_router

import services.translation_service

app = FastAPI()

app.include_router(translate_router)
app.include_router(evaluate_router)