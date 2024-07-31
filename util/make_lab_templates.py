#!/usr/bin/env python

import pathlib
import sys

from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('lab/_templates/'))
# js template
template = env.get_template('conf.js')
with open('lab/_static/conf.js', 'w') as f:
    f.write(template.render(distfile=sys.argv[1]))
    print('created lab/_static/conf.js')

# html template
template = env.get_template('form_template.html')
root = pathlib.Path('examples/lab')
for example in root.iterdir():
    setup = example.joinpath('setup.py').read_text()
    task = example.joinpath('task.py').read_text()
    check = ''
    with example.joinpath('check.py').open('r') as f:
        for line in f.readlines():
            if 'import' not in line:
                check += line
    name = example.name
    with open(f'lab/{name}.html', 'w') as f:
        f.write(
            template.render(setup=setup, task=task, check=check, name=name)
        )
        print(f'created lab/{name}.html')
