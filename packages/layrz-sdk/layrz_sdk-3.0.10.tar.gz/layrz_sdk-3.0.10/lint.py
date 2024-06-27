""" Lint files """
import argparse
import os

from pylint.lint import Run

parser = argparse.ArgumentParser(description='Lint code')
parser.add_argument('--module', type=str, help='Module to lint')
args = parser.parse_args()

IGNORE_FOLDERS = (
  '.venv',
  '.git',
  '__pycache__',
  'test.py',
)

IGNORE_EXTENSIONS = ('.pyc', )

IGNORE_FILES = ('lint.py', )

watch_files = []
for root, dirs, files in os.walk('.'):
  dirs[:] = [d for d in dirs if d not in IGNORE_FOLDERS]
  for file in files:
    if file.endswith(IGNORE_EXTENSIONS) or file in IGNORE_FILES:
      continue
    if file.endswith('.py'):
      watch_files.append(os.path.join(root, file))

if args.module:
  watch_files = [f for f in watch_files if args.module in f]

#print(f'Linting {len(watch_files)} files')

Run([
  '--rcfile=pyproject.toml',
  '--persistent=n',
  '--jobs=0',
  *watch_files,
])
