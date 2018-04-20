#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='python-clojure-shell',
      version='0.0.1',
      description='Python module to generate clojure code to be evaluated',
      author='Brian Gregg',
      author_email='biscuitalmighty@gmail.com',
      license='MIT',
      keywords=['clojure','nrepl','repl','clj'],
      packages=find_packages(),
      install_requires=['nrepl-python-client>=0.0.3', 'pyclj>=0.4.0'],
      entry_points={
          'console_scripts': [
              'pyclj-shell=clojure.shell:main'
          ]
      }
     )
