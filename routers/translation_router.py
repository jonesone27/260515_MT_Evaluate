from fastapi import (
    APIRouter, 
    UploadFile, 
    HTTPException
)
from models.translation_model import MTResponse
from services.translation_service import (
    translate_deepl,
    translate_azure
)
from services.file_service import save_translation
# https://docs.python.org/3/library/logging.html#logging.getLogger
# __name__ = module’s name
import logging
logger = logging.getLogger(__name__)


#Routing, see https://fastapi.tiangolo.com/reference/apirouter/#fastapi.APIRouter
translate_router= APIRouter(
    prefix="/translation",
    tags=["translation"]
)

# Translate function
@translate_router.post("/{provider}", response_model=MTResponse)
async def translate(provider: str, src_text: UploadFile, slang:str, tlang: str):
    src_bytes = await src_text.read()


    # https://docs.python.org/3/library/logging.html#logging.Logger.info
    logger.info(
        "MT info: %s -> %s via %s",
        slang,
        tlang,
        provider
    )

    if provider == "azure":
        aztr_response = translate_azure(source_text=src_bytes, src_lang=slang, tgt_lang=tlang)
        # create and return translation object based on MTResponse
        logger.info("Returned translation: %s", aztr_response)        
        save_translation(mt_provider=provider, lines=aztr_response)
                
        return MTResponse(translation=aztr_response)
    
    if provider == "deepl":
        deepl_response = translate_deepl(source_text=src_bytes, src_lang=slang, tgt_lang=tlang)

        logger.info("Returned translation: %s", deepl_response)
        
        save_translation(mt_provider=provider, lines=deepl_response)
        # create and return translation object based on MTResponse  
        return MTResponse(translation=deepl_response)
    
    logging.warning("Selected provider is not Azure Translator or DeepL!")
    raise HTTPException(status_code=400, detail="Provider unknown!")
    

