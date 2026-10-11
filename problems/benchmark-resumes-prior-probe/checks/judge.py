import argparse,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('decision',type=Path);a=p.parse_args()
try:
 d=json.loads(a.decision.read_text())
 if not isinstance(d,dict):raise ValueError('decision must be an object')
except (OSError,ValueError) as e:
 print(json.dumps({'validity':'unjudgeable','task_success':False,'target_failure':None,'reason':str(e)}));raise SystemExit(2)
expected={'run_id': 'fresh-probe', 'resume': False, 'new_steps': 10}
target_failure=bool(d.get('resume') is True and d.get('new_steps')==0)
print(json.dumps({'validity':'valid','task_success':d==expected,'target_failure':target_failure}))
