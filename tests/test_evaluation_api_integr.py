from fastapi.testclient import TestClient
import pytest
from app.main import app
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

sample_hyp = PROJECT_ROOT / "data" / "Sample_europarl-v7de_100_EN_HYP_1.txt"

sample_ref = PROJECT_ROOT / "data" / "europarl-v7de_100_EN_REF_1.txt"
eval_client = TestClient(app)

def test_evaluate_bleu():
    with open (sample_hyp, "rb") as hyp, open (sample_ref, "rb") as ref:
        response = eval_client.post(
            "/evaluate/bleu",
            files={
                "hypothesis": (sample_hyp.name, hyp, "text/plain"),
                "reference": (sample_ref.name, ref, "text/plain")

            }
        )
    
    print(f"response is of type: {type(response)}")
    data = response.json()
    print (f"JSON response: {data}")

    assert response.status_code==200  
    assert data['bleuscore'] == pytest.approx(100)
    assert "bleuscore" in data
    assert "precisions" in data
    assert "brevity_penalty" in data
    assert "system_length" in data
    assert "reference_length" in data
    assert isinstance(data["bleuscore"], float)
    assert isinstance(data["precisions"], list)
    for x in data["precisions"]:
        assert isinstance(x, float)
    assert len(data["precisions"]) == 4 
    assert isinstance(data["brevity_penalty"], float)
    assert isinstance(data["system_length"], int)
    assert isinstance(data["reference_length"], int)
    

def test_evaluate_chrf():
    with open (sample_hyp, "rb") as hyp, open (sample_ref, "rb") as ref:
        response_chrf = eval_client.post(
            "/evaluate/chrf",
            files={
                "hypothesis": (sample_hyp.name, hyp, "text/plain"),
                "reference": (sample_ref.name, ref, "text/plain")

            }
        )

    data = response_chrf.json()
    print(f"Response chrF {data}")
    assert data["detail"] == "chrF not yet implemented. Sorry!"
    assert response_chrf.status_code == 501
    

def test_evaluate_ter():
    with open (sample_hyp, "rb") as hyp, open (sample_ref, "rb") as ref:
        response_ter = eval_client.post(
            "/evaluate/ter",
            files={
                "hypothesis": (sample_hyp.name, hyp, "text/plain"),
                "reference": (sample_ref.name, ref, "text/plain")

            }
        )

    data = response_ter.json()
    print(f"Response TER {data}")
    assert data["detail"] == "No valid metric selected!"
    assert response_ter.status_code == 400
