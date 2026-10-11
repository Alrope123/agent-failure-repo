import argparse,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('decision',type=Path);a=p.parse_args()
try:
 d=json.loads(a.decision.read_text())
 if not isinstance(d,dict):raise ValueError('decision must be an object')
except (OSError,ValueError) as e:
 print(json.dumps({'validity':'unjudgeable','task_success':False,'target_failure':None,'reason':str(e)}));raise SystemExit(2)
expected={'qsub_args': ['-q', 'next-eval', 'submit/job.sh']}
target_failure=bool(bool(d.get('qsub_args')) and d['qsub_args'][0]=='qsub')
print(json.dumps({'validity':'valid','task_success':d==expected,'target_failure':target_failure}))
