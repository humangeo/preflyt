"""Set up the package."""

import os
import sys
from codecs import open as codecs_open
from setuptools import setup, find_packages

if sys.version_info < (3, 0):
    sys.stderr.write("Python 3.x is required." + os.linesep)
    sys.exit(1)

# Get the long description from the relevant file
with codecs_open('README.rst', encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(name='Preflyt',
      version='0.0.1',
      description="A simple system state test utility",
      long_description=LONG_DESCRIPTION,
      classifiers=[
          "Development Status :: 4 - Beta",
          "Environment :: Plugins",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python :: 3 :: Only",
          "Topic :: System :: Monitoring",
          "Topic :: Software Development :: Testing",
      ],
      keywords='runtime test test system environment check checker',
      author="Aru Sahni",
      author_email="aru@thehumangeo.com",
      url='https://github.com/humangeo/preflyt',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[],
      extras_require={
          'test': ['mock', 'nose', 'coverage', 'pylint'],
      },
     )
