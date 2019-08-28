import os
import sys
from setuptools import setup, find_packages

requires = [
    #'inputs',
]

if sys.platform == 'win32':
    requires.append('pywin32')
else:
    if os.environ.get('SWAYSOCK'):
        requires.append('i3ipc')
    if os.environ.get('WAYLAND_DISPLAY'):
        requires.append('python-uinput')

setup(name='poe-controller',
      version=0.1,
      description='TBD',
      long_description='TBD',
      author='Sunguk Lee',
      author_email='d3m3vilurr@gmail.com',
      url='https://github.com/d3m3vilurr/poe-controller',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      entry_points=dict(
          console_scripts=['poe-controller=poe_controller:__main__'],
      ),
      install_requires=requires,
      dependency_links=[
          'git+https://github.com/d3m3vilurr/inputs@empty-type_codes',
      ])
