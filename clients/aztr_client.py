import os
import uuid


azure_auth_key = os.getenv("AZURE_TRANSLATOR_KEY")
azure_endpoint = "https://api.cognitive.microsofttranslator.com"

if not azure_auth_key:
    raise RuntimeError("AZURE_TRANSLATOR_KEY environment variable not configured.")
# location, also known as region.
# required if you're using a multi-service or regional (not global) resource. It can be found in the Azure portal on the Keys and Endpoint page.
location = "westeurope"

azure_path = '/translate'
constructed_url = azure_endpoint + azure_path


headers = {
    'Ocp-Apim-Subscription-Key': azure_auth_key,
    # location required if you're using a multi-service or regional (not global) resource.
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
    }