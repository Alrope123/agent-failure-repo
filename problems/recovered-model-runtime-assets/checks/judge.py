import argparse,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('decision',type=Path);a=p.parse_args()
try:
 d=json.loads(a.decision.read_text())
 if not isinstance(d,dict):raise ValueError('decision must be an object')
except (OSError,ValueError) as e:
 print(json.dumps({'validity':'unjudgeable','task_success':False,'target_failure':None,'reason':str(e)}));raise SystemExit(2)
expected={'weights_updated': True, 'tokenizer_present': True, 'processor_present': True, 'recovered_config_preserved': True}
target_failure=bool(d.get('weights_updated') is True and (d.get('tokenizer_present') is False or d.get('processor_present') is False))
print(json.dumps({'validity':'valid','task_success':d==expected,'target_failure':target_failure}))
