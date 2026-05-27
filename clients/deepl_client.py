from pathlib import Path
import deepl

deepl_key_path = Path(__file__).parent.joinpath("../DeepL_Key.key")
deepl_auth_key = deepl_key_path.read_text(encoding="utf8").strip()

deepl_client = deepl.DeepLClient(deepl_auth_key)