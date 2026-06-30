from unittest.mock import patch, Mock, AsyncMock
import pytest
import requests
import deepl
from fastapi import HTTPException

from azure.core.exceptions import ServiceRequestTimeoutError, ServiceRequestError

from services.translation_service import translate_azure, translate_deepl
from routers.translation_router import translate




class TestProviderSelection:
    #  see https://github.com/pytest-dev/pytest-asyncio
    @pytest.mark.asyncio
    async def test_select_unavailable_provider(self):

        mock_file = AsyncMock()
        mock_file.read.return_value = b"Hallo Welt"
        
        with pytest.raises(HTTPException) as excinfo:
            await translate(provider="GoogleTranslator", src_text=mock_file, slang="de", tlang="en")

        mock_file.read.assert_called_once()

        assert excinfo.value.status_code == 400
        assert excinfo.value.detail == "Provider unknown!"




# Purpose: Testing call to translation tool without API access to the actual (online) tool 
# See https://www.youtube.com/watch?v=-F6wVOlsEAM

# only unittest requires the use of classes, see https://docs.python.org/3/library/unittest.html#basic-example
# use of classes is optional for pytest, see https://docs.pytest.org/en/stable/getting-started.html#group-multiple-tests-in-a-class
class TestAzure:
    # patch temporarily replaces requests.post from translate_azure() with a Mock object.
    #  i.e. For the duration of this test,  requests.post() does not make a network request, but calls a fake object instead.
    #  call requests.post() from services.translation_service
    @patch('services.translation_service.requests.post')
    # Because of @patch, Python automatically passes the created mock, i.e. mock_post is the fake version of requests.post
    def test_translate_azure(self, mock_post):
        # Creates a completely empty fake object.
        mock_response = Mock()
        # Create fake Azure JSON
        response_list = [{'translations': [{'text': 'I declare resumed the session of the European Parliament.', 'to': 'en'}]}]

        # This is one of the most important lines, i.e. mock_response.json() returns response_list
        # return_value configures the value to be returned upon calling the mock
        # 
        mock_response.json.return_value = response_list

        # Another critical line, equivalent to response = request.json()
        mock_post.return_value = mock_response

        src_text =  "Ich erkläre die Sitzungsperiode des Europäischen Parlaments für wiederaufgenommen".encode("utf-8")

        translation = translate_azure(source_text=src_text, src_lang="de", tgt_lang="en")

        # Verify that API was called, i.e. Was requests.post() called exactly once?
        mock_post.assert_called_once()

        # Inspect call arguments
        args, kwargs = mock_post.call_args
        print(f"args: {args}")
        print(f"kwargs: {kwargs}")

        
        assert translation == ['I declare resumed the session of the European Parliament.']

        assert kwargs["params"]["from"] == "de"
        assert kwargs["params"]["to"] == ["en"]
        assert kwargs["json"][0]["text"] == "Ich erkläre die Sitzungsperiode des Europäischen Parlaments für wiederaufgenommen"

    
    @patch('services.translation_service.requests.post')
    def test_translate_azure_exception(self, mock_post):
        
        # 1. define the mock exception
        mock_post.side_effect = requests.exceptions.ConnectionError("Azure Translator not available")


        with pytest.raises(requests.exceptions.ConnectionError) as excinfo:
            translate_azure(
                source_text=b"Guten Tag", 
                src_lang="de", 
                tgt_lang="en"
                )

        print(f"Azure mock expection: {excinfo}")
        print(f"excinfo.value type: {type(excinfo.value)}") 
        assert str(excinfo.value) == "Azure Translator not available"
        assert isinstance(excinfo.value, requests.exceptions.ConnectionError)


    # See https://azuresdkdocs.z19.web.core.windows.net/python/azure-core/latest/azure.core.html#azure.core.exceptions.ServiceRequestError
    #  See https://github.com/Azure/azure-sdk-tools/blob/f4491aed714047bc5d35ca4ee2aefccfb90ce98f/packages/python-packages/apiview-stub-generator/apistub/_vendor/core/exceptions.py#L334
    @patch('services.translation_service.requests.post')
    def test_azure_timeout(self, mock_post):
        
        mock_post.side_effect = ServiceRequestTimeoutError("Timeout - server does not respond")

        with pytest.raises(ServiceRequestTimeoutError) as excinfo:
            translate_azure(
                source_text=b"Guten Tag", 
                src_lang="de", 
                tgt_lang="en"
                )
        mock_post.assert_called_once()

        # string required as value is an object attribute
        assert str(excinfo.value) == "Timeout - server does not respond"

        #  error code 408002

    @patch('services.translation_service.requests.post')
    def test_azure_connect_exception(self, mock_post):

        mock_post.side_effect = ServiceRequestError("Connection could not be established")

        with pytest.raises(ServiceRequestError) as excinfo:
            translate_azure(
                source_text=b"Guten Tag", 
                src_lang="de", 
                tgt_lang="en"
                )
        
        mock_post.assert_called_once()

        assert str(excinfo.value) == "Connection could not be established"


# DEEPL
class TestDeepL:
    @patch('services.translation_service.deepl_client.translate_text')
    def test_translate_deepl_success(self, mock_translate):

        # 1. define how the external dependency should behave
        mock_response = Mock()

        
        # Define the mock return object only (!) for deepl_client.translate_text(), incl. the "text" attribute
        # The point is that the mock lets you execute the rest of your code.
        mock_response.text = 'I declare resumed the session of the European Parliament.'
        mock_translate.return_value = mock_response


        
        # 2. Prepare test input 
        src_text = "Ich erkläre die Sitzungsperiode des Europäischen Parlaments für wiederaufgenommen".encode("utf-8")

    
        # 3b. Execute the entire translate_deepl wrapper function (see production code), only replacing/mocking deepl_client.translate_text() as defined under 1 and returning the return value from the production translate_deepl() wrapper function
        deepl_mt = translate_deepl(source_text=src_text, src_lang="de", tgt_lang="en-gb")

        # 4. Verify behavior and output
        mock_translate.assert_called_once()

        # Verify that translate_deepl() correctly processes the mocked DeepL response object and returns the expected list (from the production translate_deepl() wrapper function).
        assert deepl_mt == ['I declare resumed the session of the European Parliament.']

        args, kwargs = mock_translate.call_args
        print(f"DeepL mock args: {args}")
        print(f"DeepL mock kwargs: {kwargs}")

        assert args[0] == "Ich erkläre die Sitzungsperiode des Europäischen Parlaments für wiederaufgenommen"

        assert kwargs["target_lang"] == "en-gb"



    @patch('services.translation_service.deepl_client.translate_text')
    def test_translate_deepl_exception(self, mock_translate):

        # Using side effects, test what happens if the DeepL API is not available

        mock_translate.side_effect = Exception("Deepl unavailable")

        with pytest.raises(Exception) as excinfo:
            translate_deepl(
                source_text="Guten Tag".encode("utf-8"), 
                src_lang="de", 
                tgt_lang="en-gb"
                )
            
        
        # See https://docs.pytest.org/en/stable/how-to/assert.html
        # Regarding the "value" attribute, see also: https://docs.pytest.org/en/stable/reference/reference.html#pytest.ExceptionInfo
        print(f"DeepL mock exception: {excinfo}")
        
        mock_translate.assert_called_once()
        assert str(excinfo.value) == "Deepl unavailable"


    @patch('services.translation_service.deepl_client.translate_text')
    def test_deepl_timeout(self, mock_translate):
        
        mock_translate.side_effect = requests.exceptions.Timeout("Timeout - server does not respond")


        with pytest.raises(requests.exceptions.Timeout) as excinfo:
    
            translate_deepl(
                source_text="Guten Tag".encode("utf-8"), 
                src_lang="de", 
                tgt_lang="en-gb"
                )
        
        mock_translate.assert_called_once()

        assert str(excinfo.value) == "Timeout - server does not respond"


    # see https://github.com/DeepLcom/deepl-python/blob/main/deepl/exceptions.py
    @patch('services.translation_service.deepl_client.translate_text')
    def test_deepl_connect_exception(self, mock_translate):

        mock_translate.side_effect = deepl.exceptions.ConnectionException(
            message="Connection to the DeepL API failed", 
            should_retry=True

        )

        with pytest.raises(deepl.exceptions.ConnectionException) as excinfo:

            translate_deepl(
                source_text="Guten Tag".encode("utf-8"), 
                src_lang="de", 
                tgt_lang="en-gb"
                )
        
        mock_translate.assert_called_once()

        assert str(excinfo.value) == "Connection to the DeepL API failed"
            
