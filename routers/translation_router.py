from fastapi import (
    APIRouter, 
    UploadFile, 
    HTTPException
)
from app.models import MTResponse
from services.translation_service import (
    translate_deepl,
    translate_azure
)

#see https://fastapi.tiangolo.com/reference/apirouter/#fastapi.APIRouter
translate_router= APIRouter(
    prefix="/translation",
    tags=["translation"]
)

@translate_router.post("/{provider}", response_model=MTResponse)
async def translate(provider: str, src_text: UploadFile, slang:str, tlang: str):
    src_bytes = await src_text.read()

    if provider == "azure":
        aztr_response = translate_azure(source_text=src_bytes, src_lang=slang, tgt_lang=tlang)
        # create and return translation object based on MTResponse  
        return MTResponse(translation=aztr_response)
    
    if provider == "deepl":
        deepl_response = translate_deepl(source_text=src_bytes, src_lang=slang, tgt_lang=tlang)
    
        # create and return translation object based on MTResponse  
        return MTResponse(translation=deepl_response)
    
    raise HTTPException(status_code=400, detail="Provider unknown!")
