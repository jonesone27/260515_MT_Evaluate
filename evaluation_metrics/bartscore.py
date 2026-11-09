# from BARTScore_Github.bart_score import BARTScorer

# from pathlib import Path

# # Only required for using ParaBank 
# # MODEL_PATH = Path(__file__).parent / "models" / "bart.pth"

# class BartScore:
#     def __init__(self):
#         self.scorer = BARTScorer(device='cpu', checkpoint='facebook/bart-large-cnn')

#         # self.scorer.load(MODEL_PATH) 

#     def score(self, ref_list, hyp_list):
        
#         return self.scorer.score(ref_list, hyp_list, batch_size=4)
        

from pathlib import Path
import sys
import os
from models.evaluation_model import BARTScore, MTMetrics

PROJECT_ROOT = Path(__file__).resolve().parent.parent


# BARTSCORE_DIR = (PROJECT_ROOT / "vendors" / "BARTScore" / "BARTScore_Github")
BARTSCORE_DIR = Path(
    os.getenv(
        "BARTSCORE_DIR",
        PROJECT_ROOT / "BARTScore"
    )
).resolve()

if not BARTSCORE_DIR.is_dir():
    raise FileNotFoundError(
        f"BARTScore repository not found: {BARTSCORE_DIR}. "
        "Clone https://github.com/neulab/BARTScore "
        "and configure BARTSCORE_DIR."
    )

# Add Bartscore dir to the list of search paths for modules (sys.path)
# see: https://docs.python.org/3/builtins/stdtypes.html#sequence.insert
sys.path.insert(0, str(BARTSCORE_DIR))

from bart_score import BARTScorer

# See https://github.com/neulab/BARTScore/blob/main/bart_score.py
class BartScore:
    def __init__(self):
        self.scorer = BARTScorer(
            device="cpu",
            checkpoint="facebook/bart-large-cnn",
        )

    # see https://arxiv.org/abs/2106.11520
    def score(self, ref_list, hyp_list):

        # calculate metrics as defined in the BARTScorer class:
        b_precis_list = self.scorer.score(
            srcs=ref_list,
            tgts=hyp_list,
            batch_size=4,
        )

        b_recall_list = self.scorer.score(
            srcs=hyp_list,
            tgts=ref_list,
            batch_size=4,
        ) 


        bart_segm_scores = []

        for i, (p_score, r_score) in enumerate(zip(b_precis_list, b_recall_list)):
            segm_f_score = (p_score + r_score)/2

            bart_segm_scores.append(
                {
                "segment_no": i,
                "segment_f_score": segm_f_score,
                "segment_precision": p_score,
                "segment_recall": r_score
                }
            )
        # print(f"mere b_precis_list: {b_precis_list}")
        # print(f"mere b_recall_list: {b_recall_list}")


        prec_sum = sum(b_precis_list)
        overall_precision = prec_sum / len(b_precis_list)

        reca_sum = sum(b_recall_list)
        overall_recall = reca_sum / len(b_recall_list)

        overall_f_score = (overall_precision + overall_recall) / 2
        
        sys_length = sum(len(hyp) for hyp in hyp_list)
        ref_length = sum(len(ref) for ref in ref_list)

        no_mtsegments_scored = len(hyp_list)

        return BARTScore(
            system_length=sys_length,
            reference_length=ref_length,
            hyp_segment_qty = no_mtsegments_scored,
            f_score=overall_f_score,
            precision=overall_precision,
            recall=overall_recall,
            segment_scores=bart_segm_scores                      

        )

