import argparse,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('decision',type=Path);a=p.parse_args()
try:
 d=json.loads(a.decision.read_text())
 if not isinstance(d,dict):raise ValueError('decision must be an object')
except (OSError,ValueError) as e:
 print(json.dumps({'validity':'unjudgeable','task_success':False,'target_failure':None,'reason':str(e)}));raise SystemExit(2)
expected={'model': 'head', 'endo': [63.8, 52.5, 55.9, 53.7], 'rex': 76.1, 'path': 50.9}
target_failure=bool(d.get('model')=='head' and d.get('endo')==[50.7,43.3,44.9,47.6] and d.get('rex')==76.1)
print(json.dumps({'validity':'valid','task_success':d==expected,'target_failure':target_failure}))
