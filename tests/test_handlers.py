import pytest
from alfred.entitys.result import AlfredResult
from alfred.handlers.implementations.mutiline_to_comma import MutilineToComma

def test_in_condition_handler():
    handler = MutilineToComma()
    result = handler.handle(["a\nb\nc"])
    assert isinstance(result, AlfredResult)
    assert "'a','b','c'" in result.items[0].arg 