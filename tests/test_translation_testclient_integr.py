from fastapi.testclient import TestClient
from app.main import app

transl_client = TestClient(app)

def test_translate():
    with open(r"J:/1_NLP_Data_Engineer/260515_MT_Evaluate/data/testclient_1sent_de.txt", "rb")  as f:
        response = transl_client.post(
            "/translation/azure", 
            files={
                "src_text": ("testclient_1sent_de.txt", f, "text/plain")
                },
            params={
                "slang": "de", 
                "tlang": "en"
                }  
            )
        print(f"response is of type: {type(response)}")
        print (f"JSON response: {response.json()['translation'][0]}")  
        assert response.json()['translation'][0]=="Hello world!"
        assert response.status_code==200


# Test for DeepL to be added!!

