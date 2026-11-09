
import pytest
from pytest import approx
from unittest.mock import patch
from fastapi import HTTPException

from models.evaluation_model import MTMetrics, EvaluationResult, BARTScore, BARTSegmentScore,COMETKIWIScore, CKiwiSegmentScore
from services.evaluation_service import evaluate_mt
from evaluation_metrics.bartscore import BartScore

class TestEvaluationServiceValidation:
    def test_diff_length(self):
        hyp_list = ["Hello"]
        src_list = ["Hallo", "morgen"]
        with pytest.raises(HTTPException) as exc_info:
            evaluate_mt(hypo_list=hyp_list, srce_list=src_list)
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "Ensure the MT and source documents contain the same number of lines!"

    def test_seg_qty(self):
        hyp_list = ["Hello", "tomorrow", "morning", "yesterday"]
        src_list = ["Hallo", "morgen", "morgen"]
        with pytest.raises(HTTPException) as exc_info:
            evaluate_mt(hypo_list=hyp_list, srce_list=src_list)
        assert exc_info.value.status_code==400
        assert exc_info.value.detail=="Ensure the MT and source documents contain the same number of lines!"


class TestEvaluationServiceCOMETKiwiRealModel:

    def test_correct_instance(self):
        hyp_list = ["Hello", "tomorrow", "morning", "yesterday"]
        src_list = ["Hallo", "morgen", "morgen", "gestern"]
        result = evaluate_mt(hypo_list=hyp_list, srce_list=src_list)
        
        
        # subresult = result.results["cometkiwi22"].segment_scores
        assert isinstance(result, EvaluationResult)

    def test_segment_score(self):
        hyp_list = ["Hello", "tomorrow", "morning", "yesterday"]
        src_list = ["Hallo", "morgen", "morgen", "gestern"]
        result = evaluate_mt(hypo_list=hyp_list, srce_list=src_list)
        sentscore_morning = result.results["cometkiwi22"].segment_scores[1].segment_score
        
        assert sentscore_morning == pytest.approx(0.807608, abs=1e-6)


    def test_system_length(self):
        hyp_list = ["Hello", "tomorrow", "morning", "yesterday"]
        src_list = ["Hallo", "morgen", "morgen", "gestern"]
        result = evaluate_mt(hypo_list=hyp_list, srce_list=src_list)
        mt_length = result.results["cometkiwi22"].system_length
        assert mt_length == 29

    def test_src_length(self):
        hyp_list = ["Hello", "tomorrow", "morning", "yesterday"]
        src_list = ["Hallo", "morgen", "morgen", "gestern"]
        result = evaluate_mt(hypo_list=hyp_list, srce_list=src_list)
        src_length = result.results["cometkiwi22"].source_length
        assert src_length == 24



class Test_Cometkiwi22_Service:

    @patch("services.evaluation_service.COMETKIWI")
    def test_evaluatemt_cometkiwi(self, mock_cometkiwi22):

        hypothesis_list = ["Hello", "tomorrow", "morning", "yesterday"]
        source_list = ["Hallo", "morgen", "morgen", "gestern"]

    # 1st return value = the mocked COMETKIWI object, 2nd RV = returned method result: 
    # "cometkiwi = COMETKIWI()
    # ckiwi_result = cometkiwi.calc_ckiwi(src_list=srce_list, hyp_list=hypo_list)"
    # prod. evaluate_mt() returns the following "mock" COMETKIWIScore: 

        mock_cometkiwi22.return_value.calc_ckiwi.return_value = COMETKIWIScore(
            system_length=29, 
            reference_length=None, 
            source_length=24, 
            hyp_segment_qty=4, 
            overall_score=0.803604930639267, 
            segment_scores=[CKiwiSegmentScore(segment_no=0, segment_score=0.840208888053894), CKiwiSegmentScore(segment_no=1, segment_score=0.8076083064079285), CKiwiSegmentScore(segment_no=2, segment_score=0.7778638601303101), CKiwiSegmentScore(segment_no=3, segment_score=0.7887386679649353)])

        expected_score = mock_cometkiwi22.return_value.calc_ckiwi.return_value
        
        score = evaluate_mt(srce_list=source_list, hypo_list=hypothesis_list)

        # evaluate_mt.assert_called_once() -> not necessary because the production evaluate_mt() is called

        assert score.results["cometkiwi22"].system_length==29
        assert score.results["cometkiwi22"].source_length==24
        assert score.results["cometkiwi22"] == expected_score

        mock_cometkiwi22.return_value.calc_ckiwi.assert_called_once_with(
            src_list=source_list, 
            hyp_list=hypothesis_list
        )

        assert list(score.results.keys()) == ["cometkiwi22"] 

        
        


    @patch("services.evaluation_service.COMETKIWI")
    def test_src_hyp_diffqty(self, mock_cometkiwi22):

        hypothesis_list = ["Hello", "tomorrow", "morning", "yesterday"]
        source_list = ["Hallo", "morgen", "morgen"]

        with pytest.raises(HTTPException) as exc_info:
            evaluate_mt(srce_list=source_list, hypo_list=hypothesis_list)
        assert exc_info.value.status_code==400
        assert exc_info.value.detail=="Ensure the MT and source documents contain the same number of lines!"
        mock_cometkiwi22.assert_not_called()


    @patch("services.evaluation_service.COMETKIWI")
    def test_call_no_ref_or_src(self, mock_cometkiwi22):

        hypothesis_list = ["Hello", "tomorrow", "morning", "yesterday"]

        with pytest.raises(HTTPException) as exc_info:
            evaluate_mt(hypo_list=hypothesis_list, refe_list=None, srce_list=None)

        assert exc_info.value.status_code==400
        assert exc_info.value.detail=="Upload the source document and/or a reference document in addition to the machine translation document for evaluation!"
        # Verify that the COMETKIWI constructor is not called
        mock_cometkiwi22.assert_not_called()



    @patch("services.evaluation_service.COMETKIWI")
    def test_call_with_ref_and_src(self, mock_cometkiwi22):

        hypothesis_list = ["Hello", "tomorrow", "morning", "yesterday"]
        reference_list = ["Hello", "tomorrow", "morning", "yesterday"]
        source_list = ["Hallo", "morgen", "morgen", "gestern"]

        with pytest.raises(HTTPException) as exc_info:
            evaluate_mt(hypo_list=hypothesis_list, refe_list=reference_list, srce_list=source_list)

        assert exc_info.value.status_code==422
        assert exc_info.value.detail=="Sorry, no metrics based on both source and reference documents available yet."
        mock_cometkiwi22.assert_not_called()


class Test_Bartscore_Service:

  # Patch the name that the code under test looks up when it runs, not necessarily the place where the class or function was originally defined!
    @patch("services.evaluation_service.BartScore")
    def test_bartscore_unittest(self, mock_bartscore):

        bartscore = mock_bartscore.return_value
        
        bartscore.score.return_value = BARTScore(system_length=39, reference_length=53, source_length=None, hyp_segment_qty=3, f_score=-1.003551552693049, precision=-0.2757626175880432, recall=-1.731340487798055, segment_scores=[BARTSegmentScore(segment_no=0, segment_f_score=-0.9190469831228256, segment_precision=-0.2736681401729584, segment_recall=-1.5644258260726929), BARTSegmentScore(segment_no=1, segment_f_score=-0.7767864763736725, segment_precision=-0.2780248522758484, segment_recall=-1.2755481004714966), BARTSegmentScore(segment_no=2, segment_f_score=-1.3148211985826492, segment_precision=-0.2755948603153229, segment_recall=-2.3540475368499756)])

        hypothesis_list = ["This is good.", "This is bad.", "This is great."]
        reference_list = ["This is pleasant", "This is unfortunate.", "This is splendid."]


        score = evaluate_mt(hypo_list=hypothesis_list, refe_list=reference_list)

        mock_bartscore.assert_called_once()
        bartscore.score.assert_called_once()
        bartscore.score.assert_called_once_with(hyp_list=hypothesis_list, ref_list=reference_list)

        # See services.evaluation_service.py:
        assert score.results["bartscore"] == bartscore.score.return_value

        assert isinstance(score, EvaluationResult)
        
 # see https://docs.python.org/3/library/unittest.mock.html#nesting-patch-decorators       
class Test_Mock_Bartscore_Cometkiwi:
    @patch("services.evaluation_service.BartScore")
    @patch("services.evaluation_service.COMETKIWI")
    def test_all_metrics(self, mock_cometkiwi22, mock_bartscore):
        hypothesis_list = ["Hello", "tomorrow", "morning"]
        reference_list = ["Hello", "tomorrow", "morning"]
        source_list = ["Hallo", "morgen", "morgen"]
        
        
        bartscore = mock_bartscore.return_value
        
        bartscore.score.return_value = bartscore.score.return_value = BARTScore(
    system_length=503,
    reference_length=503,
    source_length=None,
    hyp_segment_qty=3,
    f_score=-0.2757626175880432,
    precision=-0.2757626175880432,
    recall=-0.2757626175880432,
    segment_scores=[
        BARTSegmentScore(
            segment_no=0,
            segment_f_score=-0.2736681401729584,
            segment_precision=-0.2736681401729584,
            segment_recall=-0.2736681401729584
        ),
        BARTSegmentScore(
            segment_no=1,
            segment_f_score=-0.2780248522758484,
            segment_precision=-0.2780248522758484,
            segment_recall=-0.2780248522758484
        ),
        BARTSegmentScore(
            segment_no=2,
            segment_f_score=-0.2755948603153229,
            segment_precision=-0.2755948603153229,
            segment_recall=-0.2755948603153229
        )
    ]
)
        
        
        cometkiwi = mock_cometkiwi22.return_value
        
        cometkiwi.calc_ckiwi.return_value = cometkiwi.calc_ckiwi.return_value = COMETKIWIScore(
    system_length=503,
    reference_length=None,
    source_length=503,
    hyp_segment_qty=3,
    overall_score=0.25738932689030963,
    segment_scores=[
        CKiwiSegmentScore(
            segment_no=0,
            segment_score=0.25583040714263916
        ),
        CKiwiSegmentScore(
            segment_no=1,
            segment_score=0.22257885336875916
        ),
        CKiwiSegmentScore(
            segment_no=2,
            segment_score=0.29375872015953064
        )
    ]
)
        
        
        score = evaluate_mt(srce_list=source_list, hypo_list=hypothesis_list, refe_list=reference_list)
        
        mock_bartscore.assert_called_once()
        bartscore.score.assert_called_once_with(ref_list=reference_list, hyp_list=hypothesis_list)
        
        mock_cometkiwi22.assert_called_once()
        cometkiwi.calc_ckiwi.assert_called_once_with(src_list=source_list, hyp_list=hypothesis_list)
        
        
        assert isinstance(score, EvaluationResult)
        
         
        assert "bartscore" in score.results
        assert "cometkiwi22" in score.results
        
        assert score.results["bartscore"].hyp_segment_qty == len(hypothesis_list)
        assert score.results["cometkiwi22"].hyp_segment_qty == len(hypothesis_list)
        
        assert score.results["bartscore"].hyp_segment_qty ==  score.results["cometkiwi22"].hyp_segment_qty
        assert score.results["bartscore"].system_length ==  score.results["cometkiwi22"].system_length
        
        assert len(score.results["bartscore"].segment_scores) == len(score.results["cometkiwi22"].segment_scores)
        
        for bart, comet in zip(score.results["bartscore"].segment_scores,
                               score.results["cometkiwi22"].segment_scores):
            assert bart.segment_no == comet.segment_no
            
        
        
        
        
        
        