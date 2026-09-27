import pytest
from reliable_ai_lab import evidence_gate as m
from reliable_ai_lab.common import demo_sources

def test_expected_flags():
    r = m.run(m.sample())
    assert [x['status'] for x in r['claims']] == ['lexically_supported','numeric_review','invalid_citation','negation_review','insufficient_evidence']
    assert r['metrics']['needs_review'] == 4

@pytest.mark.parametrize('ids,status', [([], 'uncited'), (['unknown'],'invalid_citation'), (['queue'],'lexically_supported')])
def test_citation_resolution(ids,status):
    assert m.check_claim('The inference queue limit is 128 requests.',demo_sources(),ids)['status'] == status

def test_numeric_evidence_is_literal():
    r=m.check_claim('The cache time to live is 600 seconds.',demo_sources(),['cache'])
    assert r['unmatched_numbers'] == ['600']
    assert '60 seconds' in r['evidence']['quote']

def test_unrelated_never_passes_even_at_zero_threshold():
    assert m.check_claim('zebras galaxies',demo_sources(),['queue'],0)['status'] == 'insufficient_evidence'

@pytest.mark.parametrize('threshold',[-1,2,float('nan')])
def test_threshold_validation(threshold):
    with pytest.raises(ValueError): m.check_claim('test',demo_sources(),['queue'],threshold)
