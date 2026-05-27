from pathlib import Path

import uuid
aztr_key_path = Path(__file__).parent.joinpath("../Azure_Key.key")
azure_key = aztr_key_path.read_text(encoding="utf8").strip()
azure_endpoint = "https://api.cognitive.microsofttranslator.com"

# location, also known as region.
# required if you're using a multi-service or regional (not global) resource. It can be found in the Azure portal on the Keys and Endpoint page.
location = "westeurope"

azure_path = '/translate'
constructed_url = azure_endpoint + azure_path


headers = {
    'Ocp-Apim-Subscription-Key': azure_key,
    # location required if you're using a multi-service or regional (not global) resource.
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
    }