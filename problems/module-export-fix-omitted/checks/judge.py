import argparse,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('decision',type=Path);a=p.parse_args()
try:
 d=json.loads(a.decision.read_text())
 if not isinstance(d,dict):raise ValueError('decision must be an object')
except (OSError,ValueError) as e:
 print(json.dumps({'validity':'unjudgeable','task_success':False,'target_failure':None,'reason':str(e)}));raise SystemExit(2)
expected={'pbs_export': '-v', 'exported_variables': ['EVAL_SUITE', 'RUN_ID', 'MODEL_ID', 'EVAL_VENV'], 'python_env': 'next-env', 'inherited_module_table': False}
target_failure=bool(d.get('pbs_export')=='-V' and d.get('inherited_module_table') is True)
print(json.dumps({'validity':'valid','task_success':d==expected,'target_failure':target_failure}))
