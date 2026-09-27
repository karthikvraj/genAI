import copy
import pytest
from reliable_ai_lab import repair_agent as m

def test_bounded_repair_is_nonexecuting():
    r=m.run(m.sample());assert r['decision']=='awaiting_human_review'
    assert r['metrics']['attempts']==2 and r['metrics']['actions_executed']==0
    assert r['plan']['human_approval_required'] is True
    assert set(r['plan']['actions']) <= m.ALLOWED_ACTIONS

def test_audit_detects_edit():
    r=m.run(m.sample());assert m.verify_audit(r['audit'])
    changed=copy.deepcopy(r['audit']);changed[0]['errors']=[]
    assert not m.verify_audit(changed)

def test_no_domain_reasoning_is_invented():
    p=m.sample();p['plan'].pop('hypothesis');r=m.run(p)
    assert r['decision']=='stopped' and 'hypothesis' not in r['plan']

def test_repeated_plan_stops():
    r=m.run(m.sample(),planner=lambda p,e,s:p)
    assert r['decision']=='stopped' and r['metrics']['attempts']==2

def test_attempt_limit():
    p=m.sample();p['max_attempts']=1;r=m.run(p)
    assert r['decision']=='stopped' and r['metrics']['attempts']==1

def test_unsafe_llm_result_does_not_execute():
    r=m.run(m.sample(),planner=lambda *args:{'actions':['delete_everything']})
    assert r['decision']=='stopped' and r['metrics']['actions_executed']==0

@pytest.mark.parametrize('n',[0,6,-1])
def test_attempt_validation(n):
    p=m.sample();p['max_attempts']=n
    with pytest.raises(ValueError):m.run(p)

def test_local_adapter_rejects_redirects():
    import urllib.error
    with pytest.raises(urllib.error.URLError):
        m.NoRedirect().redirect_request(None,None,302,'redirect',{},'https://external.invalid')

def test_default_does_not_call_network(monkeypatch):
    import urllib.request
    def forbidden(*args,**kwargs):raise AssertionError('Network call in offline demo')
    monkeypatch.setattr(urllib.request.OpenerDirector,'open',forbidden)
    assert m.run(m.sample())['metrics']['actions_executed']==0
