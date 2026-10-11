import argparse,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('decision',type=Path);a=p.parse_args()
try:
 d=json.loads(a.decision.read_text())
 if not isinstance(d,dict):raise ValueError('decision must be an object')
except (OSError,ValueError) as e:
 print(json.dumps({'validity':'unjudgeable','task_success':False,'target_failure':None,'reason':str(e)}));raise SystemExit(2)
expected={'jobs': [{'id': 'small', 'queue': 'capacity', 'venv': 'capacity-env', 'wrapper': 'capacity-wrapper'}, {'id': 'large', 'queue': 'capacity', 'venv': 'capacity-env', 'wrapper': 'capacity-wrapper'}]}
target_failure=bool(any(x.get('queue')=='capacity' and (x.get('venv')=='next-train-env' or x.get('wrapper')=='next-wrapper') for x in d.get('jobs',[])))
print(json.dumps({'validity':'valid','task_success':d==expected,'target_failure':target_failure}))
