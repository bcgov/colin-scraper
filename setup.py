from setuptools import find_packages
from setuptools import setup

def read_requirements(filename):
    """
    Get application requirements from
    the requirements.txt file.
    :return: Python requirements
    :rtype: list
    """
    with open(filename, 'r') as req:
        requirements = req.readlines()
    install_requires = [r.strip() for r in requirements if r.find('git+') != 0]
    return install_requires

def read(filepath):
    """
    Read the contents from a file.
    :param str filepath: path to the file to be read
    :return: file contents
    :rtype: str
    """
    with open(filepath, 'r') as file_handle:
        content = file_handle.read()
    return content

REQUIREMENTS = read_requirements('requirements.txt')

setup(
    name='COLIN-screenscraper',
    version='1.0.0',
    description='This package contains the src code for the COLIN migration screenscraper',
    install_requires=REQUIREMENTS,
    packages=find_packages()
)
