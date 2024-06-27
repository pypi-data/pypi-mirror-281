from setuptools import find_packages
from distutils.core import setup

setup(
    name='Tasfers',
    version='1.0.2',
    packages=find_packages(),
    install_requires=[
        'aiofiles'
    ],
    author='Towa',
    description='A library to simplify programming',
    url='https://github.com/Tasfers/library'
)
