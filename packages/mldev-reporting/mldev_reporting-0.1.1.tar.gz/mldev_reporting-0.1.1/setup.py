from setuptools import setup
from pathlib import Path

with open("README.md", "r") as f:
  long_description = f.read()

setup(
  name="mldev_reporting",
  version="0.1.1",
  author="MLRep Team, Alexandra Maratkanova",
  author_email="dev@mlrep.org, ola.maratkanova@gmail.com",
  url="https://gitlab.com/mlrep/mldev-reporting",
  description="An extantion library for creatind reports for MLDev",
  license="Apache 2.0 license",
  long_description=long_description,
  long_description_content_type='text/markdown',
  package_dir={"mldev_reporting" : "src/mldev_reporting"},
  packages=["mldev_reporting"],
  include_requires=[
    "pandas",
   " mldev[base]",
    "docutils",
    "jinja2",
    "m2r",
    "beautifulsoup4"
  ],
  include_package_data=True,
  classifiers=[
    "License :: OSI Approved :: Apache Software License",
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "Operating System :: POSIX :: Linux",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Topic :: Scientific/Engineering :: Artificial Intelligence"
  ]
)

# python3 css_minifier.py && python3 setup.py sdist bdist_wheel && python3 clean_up.py