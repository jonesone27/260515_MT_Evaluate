from datetime import datetime
import deepl
import requests, uuid, json
from clients.aztr_client import constructed_url, headers
from clients.deepl_client import deepl_client
from pathlib import Path
import logging
logger = logging.getLogger(__name__)



def translate_deepl(source_text: bytes, src_lang:str, tgt_lang: str):
    # load source text and retrieve mt
    source_text = source_text.decode("utf-8")
    
    mt_result = deepl_client.translate_text(source_text, target_lang=tgt_lang)
    # convert MT to list for calculating BLEU
    deepl_mt = mt_result.text.splitlines()
        
    # nonempty = [ln for ln in deepl_mt if ln.strip() != ""]
    # curdate = datetime.now().strftime("%y_%m_%d_%H_%M")
    # DATA_DIR = Path(__file__).resolve().parent.parent / "data"
    # DATA_DIR.mkdir(exist_ok=True)
    # filepath = DATA_DIR / f"DeepL_{curdate}.txt"
    # # with open (filepath, "w", encoding="utf-8") as f: 
    # # with open(f"./data/DeepL_{curdate}.txt", "w", encoding="utf-8") as f:
    #     f.write("\n".join(nonempty) + ("\n" if nonempty else ""))

    return deepl_mt



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

    request = requests.post(constructed_url, params=params, headers=headers, json=body)

    # returns a list
    response = request.json()
    logger.info("Azure JSON response: %r", response)
    # print translation to console to check
    # print(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))
    azure_mt = response[0]["translations"][0]["text"].splitlines()
    logger.info("Azure response as String, %r", azure_mt)
    
    
    # export translation to file
    
    
    return azure_mt

