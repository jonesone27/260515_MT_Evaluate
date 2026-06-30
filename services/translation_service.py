import requests
from clients.aztr_client import constructed_url, headers
from clients.deepl_client import deepl_client
import logging
import time 
import deepl
logger = logging.getLogger(__name__)



# def translate_azure(source_text: Annotated[bytes, File()], slang:str, tlang: str, aztr_ref_text: Annotated[bytes | None, File()] = None):
def translate_azure(source_text: bytes, src_lang:str, tgt_lang: str):

    params = {
        'api-version': '3.0',
        'from': src_lang,
        'to': [tgt_lang]
    }
    source_text = source_text.decode("utf-8")

    # You can pass more than one object in body.
    body = [{
        'text': source_text
    }]

    try:
            
        start_time = time.perf_counter()

        response = requests.post(constructed_url, params=params, headers=headers, json=body)
        
        
        # Measure latency of API call
        elapsed = time.perf_counter() - start_time

        response.raise_for_status()

        translation = response.json()
        # print(f"response: {response}")
        # print(f"response type: {type(response)}")
        # returns a list
        # print(f"translation: {translation}")
        # response_content =response.text
        # print(f"response_content: {response_content}")
        logger.info("Azure Translation request completed in %.3f seconds", elapsed)
        # logger.info("Azure JSON response: %r", translation)
        # print translation to console to check
        # print(json.dumps(translation, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))
        azure_mt = translation[0]["translations"][0]["text"].splitlines()
        logger.debug("Azure response as String, %r", azure_mt)
            

        return azure_mt

    except requests.exceptions.RequestException:
        logger.exception(
            "Requested Azure translation from %s to %s failed!", 
            src_lang, 
            tgt_lang, 
        )
        raise

def translate_deepl(source_text: bytes, src_lang:str, tgt_lang: str):
    try:

        # load source text and retrieve mt

        source_text = source_text.decode("utf-8")
        
        start_time = time.perf_counter()
        # mt_result is an object incl. the translation returned by DeepL
        mt_result = deepl_client.translate_text(source_text, target_lang=tgt_lang)
        # convert MT to list for calculating BLEU

        elapsed = time.perf_counter() - start_time

        logger.info("DeepL request completed in %.3f seconds", elapsed)
        deepl_mt = mt_result.text.splitlines()
        
        logger.debug("DeepL response: %r", mt_result)
        logger.debug("DeepL response type: %s", type(mt_result))
        logger.debug("DeepL response attributes: %s", dir(mt_result))
    ## access the translation text from the returned DeepL object
        
        return deepl_mt

    except deepl.exceptions.DeepLException as e:
        logger.exception("DeepL translation from %s to %s failed!", 
            src_lang, 
            tgt_lang,
            )
        raise


    
    

