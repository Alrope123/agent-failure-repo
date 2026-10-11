import argparse,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('decision',type=Path);a=p.parse_args()
try:
 d=json.loads(a.decision.read_text())
 if not isinstance(d,dict):raise ValueError('decision must be an object')
except (OSError,ValueError) as e:
 print(json.dumps({'validity':'unjudgeable','task_success':False,'target_failure':None,'reason':str(e)}));raise SystemExit(2)
expected={'cli_batch': 1, 'accumulation': 16, 'derived_state_batch': 1, 'original_state_batch': 2, 'global_batch': 192, 'max_steps': 7314}
target_failure=bool(d.get('derived_state_batch')==2 and d.get('accumulation')==16)
print(json.dumps({'validity':'valid','task_success':d==expected,'target_failure':target_failure}))
