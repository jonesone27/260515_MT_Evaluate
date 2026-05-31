import pytest

from services.translation_service import translate_azure


# Integration/functionality test (FastAPI integration, internet connection, azure key, azure quota,)
def test_de_en():
    result= translate_azure(b"Hallo Welt!", "de", "en")
    assert result==['Hello world!']

def test_azure_return_string():
    result = translate_azure(source_text=b"Hallo Welt!", src_lang="de", tgt_lang="en")
    assert isinstance(result[0], str)