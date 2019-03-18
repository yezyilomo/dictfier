import os
import io
import pathlib
from setuptools import setup, find_packages

DESCRIPTION = """
    Python library to convert Python class instances(Objects) both flat and nested into a dictionary data structure. 
    It's very useful in converting Python Objects into JSON format especially for nested objects, 
    because they can't be handled well by json library
    """
REQUIRES_PYTHON = '>=2.7'
here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

setup(
    name = 'dictifier',
    version = '0.0.0',
    description = DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/yezyilomo/dictifier",
    author = 'Yezy Ilomo',
    author_email = 'yezileliilomo@hotmail.com',
    packages = find_packages(exclude=('tests','test')),
    package_data = {},
    install_requires = [],
    python_requires=REQUIRES_PYTHON,
)
