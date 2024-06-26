from setuptools import setup, find_packages

setup(
  name="mldev_reporting",
  version="0.1",
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
  include_package_data=True
)

# python3 css_minifier.py && python3 setup.py sdist bdist_wheel && python3 clean_up.py