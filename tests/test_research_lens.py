import hashlib
from reliable_ai_lab import research_lens as m

def test_every_quote_has_provenance():
    p=m.sample();r=m.run(p);sources={d['id']:d['text'] for d in p['documents']}
    assert r['excerpts']
    for e in r['excerpts']:
        assert e['quote'] in sources[e['source_id']]
        assert e['source_sha256']==hashlib.sha256(sources[e['source_id']].encode()).hexdigest()

def test_unknown_subject_abstains():
    p=m.sample();p['query']='saffron giraffe';r=m.run(p)
    assert r['decision']=='abstain' and r['extractive_note']==''

def test_duplicate_excerpts_not_repeated():
    p=m.sample();p['documents'].append({'id':'copy','text':p['documents'][3]['text']});r=m.run(p)
    assert len({x['quote'] for x in r['excerpts']})==len(r['excerpts'])

def test_source_change_changes_hash():
    p=m.sample();a=m.run(p);p['documents'][0]['text']+=' Updated.';b=m.run(p)
    assert a['source_manifest'][0]['sha256']!=b['source_manifest'][0]['sha256']
