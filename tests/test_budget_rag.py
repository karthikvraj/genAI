import pytest
from reliable_ai_lab import budget_rag as m

@pytest.mark.parametrize('budget',[1,7,15,22,38,100])
def test_hard_word_budget(budget):
    p=m.sample();p['word_budget']=budget;r=m.run(p)
    assert sum(c['words'] for c in r['context'])<=budget
    assert len(r['context'])==r['metrics']['selected_chunks']
    assert r['metrics']['selected_words']<=budget

def test_known_sources_retrieved():
    r=m.run(m.sample())
    assert {'gpu','network'} <= {x['id'] for x in r['context']}
    assert r['metrics']['source_recall']==1

def test_out_of_vocabulary_abstains():
    p=m.sample();p['query']='saffron giraffe';r=m.run(p)
    assert r['decision']=='abstain' and not r['context']

def test_budget_can_differ_from_top_k():
    p=m.sample();p['word_budget']=15;r=m.run(p)
    assert r['metrics']['fixed_top3_over_budget']
    assert r['metrics']['selected_words']<=15
