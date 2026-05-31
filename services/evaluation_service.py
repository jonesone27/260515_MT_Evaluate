# ggf. noch Metrik als Parameter übergeben?
from sacrebleu.metrics import BLEU
from models.evaluation_model import MTMetrics
from fastapi import HTTPException
import logging
logger = logging.getLogger(__name__)

# Type hints-> see https://docs.python.org/3/library/typing.html
def evaluate_mt(metric: str, mt_hyp: bytes, mt_ref: bytes) -> MTMetrics:
    mt_hyp = mt_hyp.decode("utf-8").splitlines()
    mt_ref = mt_ref.decode("utf-8").splitlines()        

    if metric == "bleu":
        bleu_obj=BLEU()
        bleuscore = bleu_obj.corpus_score(mt_hyp, [mt_ref])
        print(f"Bleuscore: {bleuscore} \n")
        bleu_metrics = MTMetrics(bleuscore=bleuscore.score, precisions=bleuscore.precisions, brevity_penalty=bleuscore.bp, system_length=bleuscore.sys_len, reference_length=bleuscore.ref_len)
        logger.info("Bleuscore: %s.", bleu_metrics)
        return bleu_metrics

    if metric == "chrf":
        exception = HTTPException(status_code=501, detail="chrF not yet implemented. Sorry!")
        logger.error("Error: %s", exception.status_code)
        raise exception

    raise HTTPException(status_code=400, detail="No valid metric selected!")

