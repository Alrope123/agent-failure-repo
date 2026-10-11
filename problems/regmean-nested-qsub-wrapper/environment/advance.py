import argparse,shutil
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('destination',type=Path);a=p.parse_args()
if not a.destination.is_dir() or not (a.destination/'fixture.json').is_file():raise SystemExit('Run setup first in an evaluator-owned disposable directory')
shutil.copyfile(Path(__file__).with_name('fixture.json'),a.destination/'fixture.json')
print('Stage 2 observations installed')
