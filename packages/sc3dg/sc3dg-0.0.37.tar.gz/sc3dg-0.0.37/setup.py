from setuptools import setup, Extension
from Cython.Build import cythonize
with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

module = Extension('sc3dg.model.dyn_util', ['sc3dg/model/dyn_util.pyx'])

setup(
    name="sc3dg",
    version="0.0.37",
    description="a toolkit for processing single cell Hi-C data",
    author="ABC",

    packages=['sc3dg', 'sc3dg.utils', 'sc3dg.analysis',  'sc3dg.commands', 'sc3dg.model'],
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'stark = sc3dg.cli:cli',
        ]}
)
