#!/usr/bin/env python3
"""Run and preserve isolated original/PQC pytest results for a Team B batch."""
from __future__ import annotations
import argparse, datetime as dt, json, subprocess, sys, xml.etree.ElementTree as ET
from importlib.metadata import version
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
TEAM=Path(__file__).resolve().parent

def run(spec: dict, kind: str) -> dict:
    rid=spec['repository_id']; slug=spec['slug']; app=ROOT/'benchmark'/'repositories'/rid
    test=f"tests/test_{slug}{'_pqc' if kind == 'pqc' else ''}.py"
    ev=ROOT/'reports'/'evidence'/rid; ev.mkdir(parents=True,exist_ok=True)
    xml=ev/f'{kind}-junit.xml'; log=ev/f'{kind}-pytest.log'
    cmd=[sys.executable,'-m','pytest',test,'-q',f'--junitxml={xml.as_posix()}']
    started=dt.datetime.now(dt.timezone.utc).isoformat()
    proc=subprocess.run(cmd,cwd=app,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    log.write_text(proc.stdout,encoding='utf-8',newline='\n')
    try:
        root=ET.parse(xml).getroot(); nodes=[root] if root.tag=='testsuite' else root.findall('.//testsuite')
        tests=sum(int(n.attrib.get('tests',0)) for n in nodes); failures=sum(int(n.attrib.get('failures',0)) for n in nodes); errors=sum(int(n.attrib.get('errors',0)) for n in nodes); skipped=sum(int(n.attrib.get('skipped',0)) for n in nodes)
    except (OSError,ET.ParseError): tests=failures=errors=skipped=None
    return {'suite':kind,'command':' '.join(cmd),'cwd':str(app),'started_utc':started,'exit_code':proc.returncode,'tests':tests,'passed':None if tests is None else tests-failures-errors-skipped,'failed':None if tests is None else failures+errors,'skipped':skipped,'log':f'reports/evidence/{rid}/{kind}-pytest.log','junit_xml':f'reports/evidence/{rid}/{kind}-junit.xml'}

def main()->int:
    p=argparse.ArgumentParser(); p.add_argument('--batch',type=int,required=True); a=p.parse_args()
    specs=json.loads((TEAM/'application_specs.json').read_text(encoding='utf-8')); specs=[s for s in specs if s['batch']==a.batch]
    if len(specs)!=10: raise SystemExit(f'expected 10 specs for batch {a.batch}, got {len(specs)}')
    results=[]
    for s in specs:
        suites=[run(s,'original'),run(s,'pqc')]
        item={'repository_id':s['repository_id'],'application_name':s['name'],'suites':suites}
        results.append(item)
        print(f"{s['repository_id']}: original={suites[0]['exit_code']} ({suites[0]['passed']}/{suites[0]['tests']}), pqc={suites[1]['exit_code']} ({suites[1]['passed']}/{suites[1]['tests']})")
    summary={'batch':a.batch,'recorded_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'python':sys.version,'dependencies':{n:version(n) for n in ('cryptography','pytest','jsonschema')},'applications':results,'total_suites':sum(len(x['suites']) for x in results),'total_tests':sum(x['tests'] or 0 for y in results for x in y['suites']),'total_passed':sum(x['passed'] or 0 for y in results for x in y['suites']),'total_failed':sum(x['failed'] or 0 for y in results for x in y['suites']),'total_skipped':sum(x['skipped'] or 0 for y in results for x in y['suites'])}
    out=TEAM/f'batch-{a.batch:02d}'/'test-results.json'; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    (TEAM/'original_test_summary.json').write_text(json.dumps({'batch':a.batch,'applications':[{'repository_id':x['repository_id'],'suite':x['suites'][0]} for x in results]},indent=2)+'\n',encoding='utf-8')
    (TEAM/'pqc_reference_test_summary.json').write_text(json.dumps({'batch':a.batch,'applications':[{'repository_id':x['repository_id'],'suite':x['suites'][1]} for x in results]},indent=2)+'\n',encoding='utf-8')
    return int(summary['total_failed'] != 0 or summary['total_suites'] != 20)
if __name__=='__main__': raise SystemExit(main())
