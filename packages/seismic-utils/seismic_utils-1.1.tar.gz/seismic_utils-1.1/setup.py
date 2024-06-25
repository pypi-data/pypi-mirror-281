from distutils.core import setup
from setuptools import find_packages

VERSION = '1.1'

setup(
    name='seismic-utils',
    version=VERSION,
    description='A python package including some seismic toolkits',
    author='Wenchen Lie',
    author_email='666@e.gzhu.edu.cn',
    install_requires=['pandas', 'dill', 'numpy', 'matplotlib'],
    packages=find_packages(),
)