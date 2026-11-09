from fastapi.testclient import TestClient
import pytest
from pytest import approx
from unittest.mock import patch
from app.main import app
from pathlib import Path
from models.evaluation_model import BARTScore, BARTSegmentScore


PROJECT_ROOT = Path(__file__).parent.parent

# Sample files
sample_hyp = PROJECT_ROOT / "data" / "WMT14DE-EN_3_en_HYP_DeepL.txt"

sample_hyp_large = PROJECT_ROOT / "data" / "WMT14DE-EN_100_en_HYP_DeepL.txt"

sample_ref = PROJECT_ROOT / "data" / "WMT14DE-EN_3_en_REF.txt"

sample_src = PROJECT_ROOT / "data" / "WMT14DE-EN_3_de_SRC.txt"

sample_hyp_empty = PROJECT_ROOT / "data" / "WMT14DE-EN_0_en_HYP.txt"

eval_client = TestClient(app)

class Test_Bartscore_integration():
# API integration test for BARTScore
    def test_bartscore(self):
        with open (sample_ref, "rb") as ref, open (sample_hyp, "rb") as hyp:
            response = eval_client.post(
                "/evaluate",
                files={
                    "hypothesis": (sample_hyp.name, hyp, "text/plain"),
                    "reference":(sample_ref.name, ref, "text/plain")                
                }
            )           
                                                                        
            response_data = response.json()
            
        
            results = response_data["results"]["bartscore"]

            assert response.status_code == 200
            assert "bartscore" in response_data["results"]
            assert "system_length" in response_data["results"]["bartscore"] 
            assert "reference_length" in response_data["results"]["bartscore"]
            assert "source_length" in response_data["results"]["bartscore"]
            assert "hyp_segment_qty" in response_data["results"]["bartscore"]
            assert "f_score" in response_data["results"]["bartscore"]
            assert "precision" in response_data["results"]["bartscore"]
            assert "recall" in response_data["results"]["bartscore"]
            assert "segment_scores" in response_data["results"]["bartscore"]
            
            assert "segment_no" in response_data["results"]["bartscore"]["segment_scores"][1]

            # Unlike readlines(), read().splitlines() does not include line breaks (see also evaluation_router.py) 
            hyp_list=[]
            with open (sample_hyp, "r", encoding="utf-8") as f:
                hyp_list.extend(f.read().splitlines())
            hyp_lines_qty = len(hyp_list)
            
            hyp_length = sum(len(hyp) for hyp in hyp_list)
            


            ref_list=[]
            with open (sample_ref, "r", encoding="utf-8") as f:
                ref_list.extend(f.read().splitlines())
            
            ref_length = sum(len(ref) for ref in ref_list)
            

            assert response_data["results"]["bartscore"]["system_length"] == hyp_length
            assert response_data["results"]["bartscore"]["reference_length"] == ref_length
            assert response_data["results"]["bartscore"]["source_length"] == None
            assert response_data["results"]["bartscore"]["hyp_segment_qty"] == hyp_lines_qty
            assert len(response_data["results"]["bartscore"]["segment_scores"]) == hyp_lines_qty

            assert response_data["results"]["bartscore"]["f_score"] <= 0
            assert response_data["results"]["bartscore"]["precision"] <= 0
            assert response_data["results"]["bartscore"]["recall"] <= 0

            assert response_data["results"]["bartscore"]["segment_scores"][1]["segment_f_score"] <=0
            assert response_data["results"]["bartscore"]["segment_scores"][1]["segment_recall"] <=0
            assert response_data["results"]["bartscore"]["segment_scores"][1]["segment_precision"] <=0



    def test_bscore_no_hyp(self):
        
    
        with open (sample_hyp_empty, "rb") as empty_hyp:
            response = eval_client.post(
                "/evaluate",
                files = {
                    "hypothesis": (sample_hyp_empty.name, empty_hyp, "text/plain")
                }
            )
    
        assert response.status_code==400
        assert response.json()=={"detail":"Upload a machine translation document. Additionally upload a reference document and/or the source document for evaluation!"}

    def test_bscore_no_ref_src(self):        
    
        with open (sample_hyp, "rb") as hyp:
            response = eval_client.post(
                "/evaluate",
                files = {
                    "hypothesis": (sample_hyp.name, hyp, "text/plain")
                }
            )
    
        assert response.status_code==400
        assert response.json()=={"detail":"Upload a reference document and/or the source document to evaluate your machine translation!"}
        
        
        
    def test_bscore_difflen_ref(self):
        
        with open (sample_hyp_large, "rb") as hyp_large, open (sample_ref, "rb") as ref:
            response = eval_client.post(
                "/evaluate",
                files = {
                    "hypothesis": (sample_hyp_large.name, hyp_large, "text/plain"),
                    "reference": (sample_ref.name, ref, "text/plain")
                }
            )
            
        assert len(sample_hyp_large.read_text(encoding="utf-8").splitlines()) != len(sample_ref.read_text(encoding="utf-8").splitlines())   
        assert response.status_code==400
        assert response.json()=={"detail":"Ensure the MT and reference documents contain the same number of lines!"}
        
        
        
        
    def test_bscore_difflen_src(self):
        
        with open (sample_hyp_large, "rb") as hyp_large, open (sample_src, "rb") as src:
            response = eval_client.post(
                "/evaluate",
                files = {
                    "hypothesis": (sample_hyp_large.name, hyp_large, "text/plain"),
                    "source": (sample_src.name, src, "text/plain")
                }
            )
           
        assert len(sample_hyp_large.read_text(encoding="utf-8").splitlines()) != len(sample_src.read_text(encoding="utf-8").splitlines())   
        assert response.status_code==400
             
        assert response.json()=={"detail":"Ensure the MT and source documents contain the same number of lines!"}
        
        
        
              
        
        
        
    # Integration test with  mocked BartScore class
    @patch("services.evaluation_service.BartScore")
    def test_bartscore_mocked(self, mock_bartscore):        

   # Add 4. API error-path tests — next

        bartscore = mock_bartscore.return_value

        bartscore.score.return_value = BARTScore(
            system_length=1234, # test value to determine if mock bartscore is called
            reference_length=4000, # test value to determine if mock bartscore is called
            source_length=None, 
            hyp_segment_qty=3, 
            f_score=-1.7615756591161091, 
            precision=-1.7918108304341633, 
            recall=-1.731340487798055, 
            segment_scores=[
                BARTSegmentScore(segment_no=0, 
            segment_f_score=-1.9560046792030334, 
            segment_precision=-2.347583532333374, 
            segment_recall=-1.5644258260726929), 
            BARTSegmentScore(segment_no=1, 
            segment_f_score=-1.4564768075942993, 
            segment_precision=-1.637405514717102, 
            segment_recall=-1.2755481004714966), 
            BARTSegmentScore(segment_no=2, 
            segment_f_score=-1.8722454905509949, 
            segment_precision=-1.3904434442520142, 
            segment_recall=-2.3540475368499756)]
            )

        

        with open (sample_ref, "rb") as ref, open (sample_hyp, "rb") as hyp:
            
            
            response = eval_client.post(
                "/evaluate",
                files={
                    "hypothesis": (sample_hyp.name, hyp, "text/plain"),
                    "reference":(sample_ref.name, ref, "text/plain")                
                }
            )
            
                       
                                                                        
            response_data = response.json()
            
            
            
            # see https://docs.python.org/3/library/pathlib.html#pathlib.Path.read_text
            expected_hyp = sample_hyp.read_text(encoding="utf-8").splitlines()
            expected_ref = sample_ref.read_text(encoding="utf-8").splitlines()
            
            # check if mock object was created 
            mock_bartscore.assert_called_once_with()
            
            
            bartscore.score.assert_called_once_with(
                ref_list=expected_ref, 
                hyp_list=expected_hyp)
            
            
            assert response.status_code == 200
            
            results = response_data["results"]["bartscore"]
            
            assert results["system_length"] == 1234
            assert results["reference_length"] == 4000
            assert results["source_length"] is None
            assert results["hyp_segment_qty"] == 3
            assert results["f_score"] == pytest.approx(-1.761575, abs=1e-6)
            assert results["precision"] == pytest.approx(-1.79181, abs=1e-6)
            assert results["recall"] == pytest.approx(-1.73134, abs=1e-6)
            assert len(results["segment_scores"]) == results["hyp_segment_qty"]
            # assert results == bartscore.score.return_value
            
            exp_segm = bartscore.score.return_value.segment_scores
            act_segm = results["segment_scores"]
            
            assert len(exp_segm) == len(act_segm)
            
            for expected, actual in zip(exp_segm, act_segm):
                assert   expected.segment_no == actual["segment_no"]
                assert   expected.segment_f_score == actual["segment_f_score"]
                assert   expected.segment_precision == actual["segment_precision"]
                assert   expected.segment_recall == actual["segment_recall"]
                
                
                
            
            

class Test_Cometkiwi22_Integration:      


    # API integration test for COMETKIWI22
    def test_cometkiwi22(self): 
        with open (sample_src, "rb") as src, open (sample_hyp, "rb") as hyp:
            response = eval_client.post(
                "/evaluate",
                files={
                    "hypothesis": (sample_hyp.name, hyp, "text/plain"),
                    "source":(sample_src.name, src, "text/plain")                
                }
            )
        
        
        # Reg. HTTPX2 responses, see https://starlette.dev/responses/#response
        response_data = response.json()
                        
        results = response_data["results"]["cometkiwi22"]
        
        assert response.status_code == 200
        assert results["source_length"] > 0
        assert results["system_length"] > 0
        assert results["overall_score"] > 0
        assert results["overall_score"] <= 1
        assert results["hyp_segment_qty"] > 0
        assert len(results["segment_scores"]) == results["hyp_segment_qty"]

        seg_scores_sum = 0
        for i in results["segment_scores"]:
            seg_scores_sum += i["segment_score"]

        test_value = seg_scores_sum / results["hyp_segment_qty"]
    # See https://docs.pytest.org/en/stable/reference/reference.html#pytest.approx
        assert test_value == approx(results["overall_score"], abs=1e-6)





class Test_Metrics_Ref_Src_Hyp_All:

    def test_all_metrics(self): 
        with open (sample_ref, "rb") as ref, open (sample_src, "rb") as src, open (sample_hyp, "rb") as hyp:
            response = eval_client.post(
                "/evaluate",
                files={
                    "hypothesis": (sample_hyp.name, hyp, "text/plain"),
                    "source":(sample_src.name, src, "text/plain"),
                    "reference":(sample_ref.name, ref, "text/plain")                
                }
            )
        
        
        assert response.status_code == 200
        
        response_data = response.json()
        
        assert "bartscore" in response_data["results"]
        assert "cometkiwi22" in response_data["results"]
        
        hyp_list=[]
        with open (sample_hyp, "r", encoding="utf-8") as f:
            hyp_list.extend(f.read().splitlines())
        hyp_lines_qty = len(hyp_list)
        
        hyp_length = sum(len(hyp) for hyp in hyp_list)
        
        
        
        ref_list=[]
        with open (sample_ref, "r", encoding="utf-8") as f:
            ref_list.extend(f.read().splitlines())
        
        ref_length = sum(len(ref) for ref in ref_list)
        
        src_list=[]
        with open (sample_src, "r", encoding="utf-8") as f:
            src_list.extend(f.read().splitlines())
        
        src_length = sum(len(ref) for ref in src_list)
        
        
        
        
        
        #assert bartscore
        bartscore_results = response_data["results"]["bartscore"]
        assert bartscore_results["system_length"] == response_data["results"]["cometkiwi22"]["system_length"]
        
        assert "bartscore" in response_data["results"]
        assert "system_length" in bartscore_results 
        assert "reference_length" in bartscore_results
        assert "source_length" in bartscore_results
        assert "hyp_segment_qty" in bartscore_results
        assert "f_score" in bartscore_results
        assert "precision" in bartscore_results
        assert "recall" in bartscore_results
        assert "segment_scores" in bartscore_results
        assert "segment_no" in bartscore_results["segment_scores"][1]
        assert bartscore_results["system_length"] == hyp_length
        assert bartscore_results["reference_length"] == ref_length
        assert bartscore_results["source_length"] is None
        assert bartscore_results["hyp_segment_qty"] == hyp_lines_qty
        assert len(bartscore_results["segment_scores"]) == hyp_lines_qty
        
        assert bartscore_results["f_score"] <= 0
        assert bartscore_results["precision"] <= 0
        assert bartscore_results["recall"] <= 0
        
        assert bartscore_results["segment_scores"][1]["segment_f_score"] <=0
        assert bartscore_results["segment_scores"][1]["segment_recall"] <=0
        assert bartscore_results["segment_scores"][1]["segment_precision"] <=0
        
        # Check correct enumeration 
        for i, segment in enumerate(bartscore_results["segment_scores"]):
            segment["segment_no"] == i
        
        
        # assert cometkiwi22
        cometkiwi_results = response_data["results"]["cometkiwi22"]
        
        assert "cometkiwi22" in response_data["results"]
        assert "system_length" in cometkiwi_results 
        assert "reference_length" in cometkiwi_results
        assert "source_length" in cometkiwi_results
        assert "hyp_segment_qty" in cometkiwi_results
        assert "overall_score" in cometkiwi_results
        assert "segment_scores" in cometkiwi_results    
        
        assert response.status_code == 200
        assert cometkiwi_results["source_length"] > 0
        assert cometkiwi_results["reference_length"] is None
        assert cometkiwi_results["system_length"] > 0
        assert cometkiwi_results["overall_score"] > 0
        assert cometkiwi_results["overall_score"] <= 1
        assert cometkiwi_results["hyp_segment_qty"] > 0
        assert len(cometkiwi_results["segment_scores"]) == cometkiwi_results["hyp_segment_qty"]
        assert cometkiwi_results["source_length"] == src_length
        
        #check correct enumeration
        
        for i, segment in enumerate(cometkiwi_results["segment_scores"]):
            segment["segment_no"] == i 
        
        seg_scores_sum = 0
        for i in cometkiwi_results["segment_scores"]:
            seg_scores_sum += i["segment_score"]
        
        test_value = seg_scores_sum / cometkiwi_results["hyp_segment_qty"]
        # See https://docs.pytest.org/en/stable/reference/reference.html#pytest.approx
        assert test_value == approx(cometkiwi_results["overall_score"], abs=1e-6)
        
        
    def test_diff_length_src_hyp_ref(self):
        with open (sample_ref, "rb") as ref, open (sample_src, "rb") as src, open (sample_hyp_large, "rb") as hyp:
                    response = eval_client.post(
                        "/evaluate",
                        files={
                            "hypothesis": (sample_hyp_large.name, hyp, "text/plain"),
                            "source":(sample_src.name, src, "text/plain"),
                            "reference":(sample_ref.name, ref, "text/plain")                
                        }
                    )
                
        hypo_list = sample_hyp_large.read_text(encoding="utf-8").splitlines()
        refe_list = sample_ref.read_text(encoding="utf-8").splitlines()
        srce_list = sample_src.read_text(encoding="utf-8").splitlines()
          
        assert response.status_code == 422
        assert response.json()["detail"] == f"Ensure the MT, source and reference documents contain the same number of lines!\n MT={len(hypo_list)} lines, REF={len(refe_list)} lines, SRC={len(srce_list)} lines"
           