# Calls the relevant evaluation metrics

# ggf. noch Metrik als Parameter übergeben?
from sacrebleu.metrics import BLEU
from models.evaluation_model import EvaluationResult
from evaluation_metrics.cometkiwi22 import COMETKIWI
from evaluation_metrics.bartscore import BartScore


from fastapi import HTTPException
import logging
logger = logging.getLogger(__name__)

# Type hints-> see https://docs.python.org/3/library/typing.html


def evaluate_mt(
        hypo_list: list[str],
        refe_list: list[str] | None = None,
        srce_list: list[str] | None = None
):

    if hypo_list is None: 
        raise HTTPException(status_code=400, detail="Upload the machine translation document in addition to at least the source document or a reference document")
    results = {}


    
    if srce_list is not None and refe_list is not None: 
        if (len(hypo_list) != len(refe_list)) or (len(srce_list) != len(hypo_list)):
            raise HTTPException(status_code=422, detail=f"Ensure the MT, source and reference documents contain the same number of lines!\n MT={len(hypo_list)} lines, REF={len(refe_list)} lines, SRC={len(srce_list)} lines")
        
        bartscore = BartScore()
        bscore_results = bartscore.score(ref_list=refe_list, hyp_list=hypo_list)
        results["bartscore"] = bscore_results
                
                
        cometkiwi = COMETKIWI()
        ckiwi_result = cometkiwi.calc_ckiwi(src_list=srce_list, hyp_list=hypo_list)
        results["cometkiwi22"] = ckiwi_result
        
        return EvaluationResult(results=results)
            
            
        
        

    elif refe_list is not None: 
        if len(hypo_list) != len(refe_list):
            raise HTTPException(status_code=400, detail="Ensure the MT and reference documents contain the same number of lines!")
        bartscore = BartScore()

        bscore_results = bartscore.score(ref_list=refe_list, hyp_list=hypo_list)

        results["bartscore"] = bscore_results

        return EvaluationResult(results=results)



    elif srce_list is not None:
        if len(srce_list) != len(hypo_list):
            raise HTTPException(status_code=400, detail="Ensure the MT and source documents contain the same number of lines!")
            
        
        cometkiwi = COMETKIWI()
        ckiwi_result = cometkiwi.calc_ckiwi(src_list=srce_list, hyp_list=hypo_list)
      
        results["cometkiwi22"] = ckiwi_result

        return EvaluationResult(results=results)
  
    raise HTTPException(status_code=400, detail="Upload the source document and/or a reference document in addition to the machine translation document for evaluation!")


# def evaluate_mt(metric: str, mt_hyp: bytes, mt_ref: bytes) -> MTMetrics:
#     mt_hyp = mt_hyp.decode("utf-8").splitlines()
#     mt_ref = mt_ref.decode("utf-8").splitlines()        

#     if metric == "bleu":
#         bleu_obj=BLEU()
#         bleuscore = bleu_obj.corpus_score(mt_hyp, [mt_ref])
#         print(f"Bleuscore: {bleuscore} \n")
#         bleu_metrics = MTMetrics(bleuscore=bleuscore.score, precisions=bleuscore.precisions, brevity_penalty=bleuscore.bp, system_length=bleuscore.sys_len, reference_length=bleuscore.ref_len)
#         logger.info("Bleuscore: %s.", bleu_metrics)
#         return bleu_metrics

#     if metric == "chrf":
#         exception = HTTPException(status_code=501, detail="chrF not yet implemented. Sorry!")
#         logger.error("Error: %s", exception.status_code)
#         raise exception

#     if metric == "bartscore":
#         bartscore_metric = bartscore.BARTScore()
#         bartscore_result = bartscore_metric.score(ref_text=mt_ref, hyp_text=mt_hyp)
#         return bartscore_result
    
#     # if metric == "cometkiwi":
        

#     raise HTTPException(status_code=400, detail="No valid metric selected!")

