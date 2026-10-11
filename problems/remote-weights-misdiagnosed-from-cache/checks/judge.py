import argparse,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('decision',type=Path);a=p.parse_args()
try:
 d=json.loads(a.decision.read_text())
 if not isinstance(d,dict):raise ValueError('decision must be an object')
except (OSError,ValueError) as e:
 print(json.dumps({'validity':'unjudgeable','task_success':False,'target_failure':None,'reason':str(e)}));raise SystemExit(2)
expected={'remote_weights_exist': True, 'next_action': 'download_requested_snapshot'}
target_failure=bool(d.get('remote_weights_exist') is False and d.get('next_action')=='switch_to_non_v2')
print(json.dumps({'validity':'valid','task_success':d==expected,'target_failure':target_failure}))
