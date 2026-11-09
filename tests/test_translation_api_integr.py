from fastapi.testclient import TestClient
from app.main import app
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

test_file = PROJECT_ROOT / "data" / "testclient_1sent_de.txt"
transl_client = TestClient(app)



def test_translate_azure():
    with open(test_file, "rb")  as f:
        response = transl_client.post(
            "/translation/azure", 
            files={
                "src_text": (test_file.name, f, "text/plain")
                },
            params={
                "slang": "de", 
                "tlang": "en"
                }  
            )
        
         
        assert response.status_code==200
        assert isinstance(response.json()["translation"], list)
        assert len(response.json()["translation"]) > 0


# Test for DeepL to be added!!
def test_translate_deepl():
    with open(test_file, "rb")  as f:
        response = transl_client.post(
            "/translation/deepl", 
            files={
                "src_text": (test_file.name, f, "text/plain")
                },
            params={
                "slang": "de", 
                "tlang": "en-gb"
                }  
            )
        
         
        assert response.status_code==200
        assert isinstance(response.json()["translation"], list)
        assert len(response.json()["translation"]) > 0
        





def test_translate_provider_x():
    with open(test_file, "rb")  as f:
        response = transl_client.post(
            "/translation/GoogleTranslate", 
            files={
                "src_text": (test_file.name, f, "text/plain")
                },
            params={
                "slang": "de", 
                "tlang": "en"
                }  
            )
        
         
        assert response.status_code==400
        assert response.json()["detail"]=="Provider unknown!"
