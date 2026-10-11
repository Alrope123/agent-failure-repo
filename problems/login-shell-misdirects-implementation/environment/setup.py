import argparse,shutil
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('destination',type=Path);a=p.parse_args()
a.destination.mkdir(mode=0o700,parents=False,exist_ok=False)
shutil.copyfile(Path(__file__).with_name('fixture-stage1.json'),a.destination/'fixture.json')
print(a.destination.resolve())
