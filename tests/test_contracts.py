import copy
import json
import pytest
from reliable_ai_lab.registry import PROJECTS, get_project
from reliable_ai_lab.common import number, integer, matrix, documents, fingerprint, sentences

@pytest.mark.parametrize('name', list(PROJECTS))
def test_reproducible_json_without_input_mutation(name):
    module = get_project(name)
    payload = module.sample(7)
    before = copy.deepcopy(payload)
    first = module.run(payload)
    assert payload == before
    assert first == module.run(module.sample(7))
    assert first['project'] == name
    assert first['limitations'] and isinstance(first['metrics'], dict)
    json.dumps(first, allow_nan=False)

@pytest.mark.parametrize('name', list(PROJECTS))
def test_missing_input_is_rejected(name):
    with pytest.raises(ValueError):
        get_project(name).run({})

@pytest.mark.parametrize('value', [None, True, False, '1', float('nan'), float('inf'), -float('inf'), [], {}])
def test_invalid_number(value):
    with pytest.raises(ValueError):
        number(value, 'value')

@pytest.mark.parametrize('value', [0, -1, 1.5, 10001])
def test_invalid_integer(value):
    with pytest.raises(ValueError):
        integer(value, 'value')

@pytest.mark.parametrize('value', [[], [1, 2], [[float('nan')]], [[float('inf')]], [[1], [1, 2]], [[[1]]]])
def test_invalid_matrix(value):
    with pytest.raises(ValueError):
        matrix(value, 'value')

def test_valid_common_primitives():
    assert number(0, 'x', 0, 1) == 0
    assert integer(3.0, 'x') == 3
    assert matrix([[1, 2]] , 'x').shape == (1, 2)
    assert fingerprint({'a': 1, 'b': 2}) == fingerprint({'b': 2, 'a': 1})
    assert sentences('Latency is 1.25 ms. Check again.') == ['Latency is 1.25 ms.', 'Check again.']

@pytest.mark.parametrize('value', [[], None, [{'id': 'a', 'text': ''}], [{'id': 'a', 'text': 'one'}, {'id': 'a', 'text': 'two'}]])
def test_invalid_documents(value):
    with pytest.raises(ValueError):
        documents(value)
