from pathlib import Path
import deepl
import os 

deepl_auth_key = os.getenv("DEEPL_KEY")

deepl_client = deepl.DeepLClient(deepl_auth_key)