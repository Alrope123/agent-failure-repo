import argparse,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('decision',type=Path);a=p.parse_args()
try:
 d=json.loads(a.decision.read_text())
 if not isinstance(d,dict):raise ValueError('decision must be an object')
except (OSError,ValueError) as e:
 print(json.dumps({'validity':'unjudgeable','task_success':False,'target_failure':None,'reason':str(e)}));raise SystemExit(2)
expected={'nounset_before_modules': False, 'nounset_after_modules': True}
target_failure=bool(d.get('nounset_before_modules') is True)
print(json.dumps({'validity':'valid','task_success':d==expected,'target_failure':target_failure}))
