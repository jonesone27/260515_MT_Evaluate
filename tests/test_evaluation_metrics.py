
import pytest
from pytest import approx
from unittest.mock import patch

from models.evaluation_model import BARTScore
from evaluation_metrics.bartscore import BartScore


class Test_Bartscore:       
    
    # "Smoke test" (no patching)
    def test_bartscore_smoke(self):
        hypothesis_list = [
        "Schools are being urged to place greater emphasis on mathematics, spelling and grammar", 
        "In English literature lessons, pupils will in future be required to study at least one play by Shakespeare, a 19th-century novel, Romantic poetry and contemporary British novels from 1914 onwards.", 
        "‘Unseen texts’ will also be included in the exam to encourage a wider range of reading."
        ]

        reference_list = [
            "Schools urged to focus more on maths, spelling and grammar", 
        "English literature courses will require pupils to study at least one Shakespeare play, a 19th century novel, Romantic poetry and contemporary British fiction from 1914 onwards.", 
        "The exam will also feature 'unseen texts' to encourage wider reading;"

        ]

        bartscoreunit = BartScore()
        result = bartscoreunit.score(ref_list=reference_list, hyp_list=hypothesis_list)
        assert isinstance(result, BARTScore)
        assert isinstance(result, BARTScore)
        assert result.hyp_segment_qty == len(hypothesis_list)
        assert len(result.segment_scores) == len(hypothesis_list)
        
        
        
        
        
              
    @patch("evaluation_metrics.bartscore.BARTScorer")
    def test_bartscorer_unittest(self, mock_bartscorer):


        # Set up a mock Bartscorer object (based on BARTScorer from the original bartscore file (GitHub), see bartscore.py)
        mock_scorer = mock_bartscorer.return_value

        # Reg. side effects, see https://docs.python.org/3/library/unittest.mock.html#quick-guide
        mock_scorer.score.side_effect = [
            [-0.2736681401729584, -0.2780248522758484, -0.2755948603153229],
            [-1.5644258260726929, -1.2755481004714966, -2.3540475368499756]
        ]

        # Instatiate the productive BartScore class defined as part of this platform
        bartscorer = BartScore()

        hypothesis_list = ["This is good.", "This is bad.", "This is great."]
        reference_list = ["This is pleasant", "This is unfortunate.", "This is splendid."]
        
        # See https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.side_effect
        # The mere BartScore model only return precision and recall for each hyp/ref segment pair

        result =  bartscorer.score(ref_list=reference_list, hyp_list=hypothesis_list)

        assert result.precision == pytest.approx(-0.2757626, abs=1e-6)
        assert result.recall == pytest.approx(-1.73134048, abs=1e-6)
        assert result.f_score == pytest.approx(-1.003551, abs=1e-6)
        assert len(result.segment_scores) == 3

        segm_results_1 = result.segment_scores[1] 
        assert segm_results_1.segment_f_score == approx(-0.776786, abs=1e-6)
        assert segm_results_1.segment_precision== approx(-0.278024, abs=1e-6)
        assert segm_results_1.segment_recall == approx(-1.275548, abs=1e-6)

        assert (segm_results_1.segment_recall + segm_results_1.segment_precision)/2 == approx(segm_results_1.segment_f_score, abs=1e-6)

        assert mock_scorer.score.call_count == 2

        # Check if the mocked scorer.score function (see bartscore.py) was called to return precision and recall as defined above

        # b_precis_list
        mock_scorer.score.assert_any_call(
            srcs=reference_list,
            tgts=hypothesis_list,
            batch_size=4)

        # b_recall_list
        mock_scorer.score.assert_any_call(
            srcs=hypothesis_list,
            tgts=reference_list,
            batch_size=4,
        ) 
     

       

  



# def test_identical_text_returns_high_bleu_score():
#     result = evaluate_mt(metric="bleu", mt_hyp=b"I declare resumed the session of the European Parliament adjourned.", mt_ref=b"I declare resumed the session of the European Parliament adjourned.")
#     assert isinstance(result, MTMetrics) 
#     assert result.bleuscore > 99 

# def test_different_text_returns_low_bleu_score():
#     result = evaluate_mt(metric="bleu", mt_hyp=b"The European Parliament session is resumed.", mt_ref=b"I declare resumed the session of the European Parliament.")
#     assert isinstance(result, MTMetrics) 
#     assert result.bleuscore < 50 

# def test_chrf_501():    
#     with pytest.raises(HTTPException) as exc_info:
#         evaluate_mt(metric="chrf", mt_hyp=b"Hello World!", mt_ref=b"Hello World!")
#     assert exc_info.value.status_code==501
#     assert exc_info.value.detail=="chrF not yet implemented. Sorry!"

# def test_metric_invalid():
#     with pytest.raises(HTTPException) as exc_info:
#         evaluate_mt(metric="TER", mt_hyp=b"Hello World!", mt_ref=b"Hello World!")
#     assert exc_info.value.status_code==400