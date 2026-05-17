from fastapi import FastAPI, File, UploadFile
import deepl
from pathlib import Path
from typing import Annotated
from sacrebleu.metrics import BLEU, CHRF, TER


app = FastAPI()
#DeepL config
key_path = Path(__file__).parent.joinpath("../DeepL_Key.key")
auth_key = key_path.read_text(encoding="utf8").strip()

deepl_client = deepl.DeepLClient(auth_key)




# # language combinations
# Create a (FastAPI/Python) object model?



# Dateipfad als Parameter
@app.post("/translate", response_model=str)
def translate_text(source_text: str | None, tlang):
    result = deepl_client.translate_text(source_text, target_lang=tlang)
    print(result.text)
    return result
# async def translate_text(payload: TranslationRequest):
#     result = await translation_service.translate(
#         text=payload.text,
#         target_lang=payload.target_lang
#     )

#     return result

# File upload in FastAPI, see https://fastapi.tiangolo.com/tutorial/request-files/?h=file#define-file-parameters
# https://docs.python.org/3/library/typing.html#typing.Annotated
# decoding, see https://realpython.com/convert-python-bytes-to-strings/
@app.post("/translate/files")
async def translate_doc(source_text: Annotated[bytes, File()], tlang, ref_text: Annotated[bytes, File()]):
    # load source text and retrieve mt
    source_text = source_text.decode("utf-8")
    mt_result = deepl_client.translate_text(source_text, target_lang=tlang)
    # convert MT to list for calculating BLEU
    hyp_bleu = mt_result.text.splitlines()
    print("Machine translation (DeepL):")
    # for x in hyp_bleu:
    #     print(x)
    print(hyp_bleu)
    # remove any empty lines from mt to ensure proper BLEU comparison/calculation
    # https://docs.python.org/3/library/stdtypes.html#str.join
    
    nonempty = [ln for ln in hyp_bleu if ln.strip() != ""]
    with open("./data/target.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(nonempty) + ("\n" if nonempty else ""))
    # load ref text
    ref_bleu = ref_text.decode("utf-8").splitlines()
    # for n in ref_bleu:
    #      print(n)
    print(ref_bleu)

    # calculate BLEU
    bleu=BLEU()
    bleuscore = bleu.corpus_score(hyp_bleu, [ref_bleu])
    print(f"Bleuscore: {bleuscore} \n")
    
    

    # return result (see https://github.com/mjpost/sacrebleu/blob/master/sacrebleu/metrics/bleu.py#L293)
    #  system length = length of hypothesis
    return {
        "bleuscore": bleuscore.score,
        "precisions": bleuscore.precisions,
        "brevity_penalty": bleuscore.bp,
        "system_length": bleuscore.sys_len,
        "reference_length": bleuscore.ref_len
    }


# with open("J:/1_NLP_Data_Engineer/260515_MT_Evaluate/data/europarl-v7de_100.txt") as f:
#     source_text = f.read()

