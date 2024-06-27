from distutils.core import setup
from setuptools import find_packages

from SeismicUtils import VERSION

setup(
    name='seismic-utils',
    version=VERSION,
    description='A python package including some seismic toolkits',
    author='Wenchen Lie',
    author_email='666@e.gzhu.edu.cn',
    install_requires=['pandas', 'dill', 'numpy', 'matplotlib', 'scipy'],
    packages=find_packages(),
)