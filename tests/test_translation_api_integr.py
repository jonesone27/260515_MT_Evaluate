from fastapi.testclient import TestClient
from app.main import app
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

test_file = PROJECT_ROOT / "data" / "testclient_1sent_de.txt"
transl_client = TestClient(app)



def test_translate():
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
        print(f"response is of type: {type(response)}")
        print (f"JSON response: {response.json()['translation'][0]}")  
        assert response.status_code==200
        assert response.json()['translation'][0]=="Hello world!"


# Test for DeepL to be added!!

