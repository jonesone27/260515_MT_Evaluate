# ggf. noch Metrik als Parameter übergeben?
from sacrebleu.metrics import BLEU
from app.models import MTMetrics
from fastapi import HTTPException
# Type hints-> see https://docs.python.org/3/library/typing.html
def evaluate_mt(metric: str, mt_hyp: bytes, mt_ref: bytes) -> MTMetrics:
    mt_hyp = mt_hyp.decode("utf-8").splitlines()
    mt_ref = mt_ref.decode("utf-8").splitlines()        

    if metric == "bleu":
        bleu_obj=BLEU()
        bleuscore = bleu_obj.corpus_score(mt_hyp, [mt_ref])
        print(f"Bleuscore: {bleuscore} \n")
        new_bleu = MTMetrics(bleuscore=bleuscore.score, precisions=bleuscore.precisions, brevity_penalty=bleuscore.bp, system_length=bleuscore.sys_len, reference_length=bleuscore.ref_len)
        return new_bleu

    if metric == "chrf":
        raise HTTPException(status_code=501, detail="chrF not yet implemented. Sorry!")

    raise HTTPException(status_code=400, detail="No valid metric selected!")

