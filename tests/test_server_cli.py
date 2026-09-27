import http.client
import json
import threading
import pytest
from reliable_ai_lab.server import LocalServer, Handler
from reliable_ai_lab.__main__ import main
from reliable_ai_lab.registry import PROJECTS, get_project

@pytest.fixture(scope='module')
def port():
    server=LocalServer(('127.0.0.1',0),Handler)
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    yield server.server_port
    server.shutdown();server.server_close();thread.join()

def request(port,method,path,body=None,headers=None):
    conn=http.client.HTTPConnection('127.0.0.1',port,timeout=20)
    conn.request(method,path,body=body,headers=headers or {})
    response=conn.getresponse();raw=response.read();status=response.status
    conn.close();return status,raw

@pytest.mark.parametrize('name',list(PROJECTS))
def test_browser_api_runs_every_project(port,name):
    status,raw=request(port,'GET','/api/sample/'+name)
    assert status==200
    status,result=request(port,'POST','/api/run/'+name,raw,{'Content-Type':'application/json','X-Lab-Request':'1'})
    assert status==200 and json.loads(result)['project']==name

@pytest.mark.parametrize('headers', [{'Host':'evil.example'}, {'Origin':'https://evil.example'}, {'Sec-Fetch-Site':'cross-site'}])
def test_cross_origin_denied(port,headers):
    assert request(port,'GET','/api/projects',headers=headers)[0]==403

@pytest.mark.parametrize('path',['/../../etc/passwd','/favicon.ico','/api/nonexistent'])
def test_no_arbitrary_file_access(port,path):
    assert request(port,'GET',path)[0]==404

def test_homepage_and_security_headers(port):
    status,body=request(port,'GET','/')
    assert status==200 and b'Ship AI.' in body and b'<textarea' in body

def test_missing_request_header(port):
    assert request(port,'POST','/api/run/evidence-gate','{}',{'Content-Type':'application/json'})[0]==403

@pytest.mark.parametrize('body',['{','[]','{"threshold":NaN}','null'])
def test_malformed_input(port,body):
    assert request(port,'POST','/api/run/evidence-gate',body,{'Content-Type':'application/json','X-Lab-Request':'1'})[0]==400

def test_media_type_check(port):
    assert request(port,'POST','/api/run/evidence-gate','{}',{'Content-Type':'text/plain','X-Lab-Request':'1'})[0]==415

def test_cli_json_roundtrip(tmp_path,capsys):
    name=next(iter(PROJECTS));sample=tmp_path/'input.json';output=tmp_path/'result.json'
    assert main(['sample',name,'--output',str(sample)])==0
    assert main(['run',name,'--input',str(sample),'--output',str(output)])==0
    assert json.loads(output.read_text())['project']==name
    assert main(['list'])==0
    assert name in capsys.readouterr().out

def test_cli_bad_json(tmp_path,capsys):
    path=tmp_path/'bad.json';path.write_text('{')
    assert main(['run',next(iter(PROJECTS)),'--input',str(path)])==2
    assert 'Error:' in capsys.readouterr().err
