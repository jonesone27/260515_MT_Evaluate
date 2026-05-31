
import pytest
from fastapi import HTTPException

from models.evaluation_model import MTMetrics
from services.evaluation_service import evaluate_mt

def test_identical_text_returns_high_bleu_score():
    result = evaluate_mt(metric="bleu", mt_hyp=b"I declare resumed the session of the European Parliament adjourned.", mt_ref=b"I declare resumed the session of the European Parliament adjourned.")
    assert isinstance(result, MTMetrics) 
    assert result.bleuscore > 99 

def test_different_text_returns_low_bleu_score():
    result = evaluate_mt(metric="bleu", mt_hyp=b"The European Parliament session is resumed.", mt_ref=b"I declare resumed the session of the European Parliament.")
    assert isinstance(result, MTMetrics) 
    assert result.bleuscore < 50 

def test_chrf_501():    
    with pytest.raises(HTTPException) as exc_info:
        evaluate_mt(metric="chrf", mt_hyp=b"Hello World!", mt_ref=b"Hello World!")
    assert exc_info.value.status_code==501
    assert exc_info.value.detail=="chrF not yet implemented. Sorry!"

def test_metric_invalid():
    with pytest.raises(HTTPException) as exc_info:
        evaluate_mt(metric="TER", mt_hyp=b"Hello World!", mt_ref=b"Hello World!")
    assert exc_info.value.status_code==400