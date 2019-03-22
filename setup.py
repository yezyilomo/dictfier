import sys
import os
import io
from setuptools import setup, find_packages

DESCRIPTION = """
    Python library to convert Python class instances(Objects) both flat and nested into a dictionary data structure. 
    It's very useful in converting Python Objects into JSON format especially for nested objects, 
    because they can't be handled well by json library
    """
REQUIRES_PYTHON = '>=2.7'
here = os.path.abspath(os.path.dirname(__file__))


# =============================================================================
# Convert README.md to README.rst for pypi
# Need to install both pypandoc and pandoc 
# - pip insall pypandoc
# - https://pandoc.org/installing.html
# =============================================================================
try:
    from pypandoc import convert

    def read_md(f):
        return convert(f, 'rst')
except:
    print('Warning: pypandoc module not found, unable to convert README.md to RST')
    print('Unless you are packaging this module for distribution you can ignore this error')

    def read_md(f):
        return DESCRIPTION

setup(
    name = 'dictfier',
    version = '1.1.8',
    description = DESCRIPTION,
    long_description = read_md('README.md'),
    long_description_content_type = 'text/markdown',
    url = "https://github.com/yezyilomo/dictfier",
    author = 'Yezy Ilomo',
    author_email = 'yezileliilomo@hotmail.com',
    packages = find_packages(exclude=('tests','test')),
    package_data = {},
    install_requires = [],
    python_requires = REQUIRES_PYTHON,
    test_suite = "tests",
)
