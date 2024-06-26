from setuptools import setup, find_packages,Extension

import numpy as np
numpy_includes = np.get_include()
with open('requirements.txt') as f:
    install_requires = f.read().splitlines()



setup(
    name="sc3dg",
    version="0.0.39",
    description="a toolkit for processing single cell Hi-C data",
    author="ABC",
    ext_modules=[
        Extension("sc3dg.model.dyn_util", ["sc3dg/model/dyn_util.c"], libraries=["m"], include_dirs=[numpy_includes]),
    ],
    packages=['sc3dg', 'sc3dg.utils', 'sc3dg.analysis',  'sc3dg.commands', 'sc3dg.model'],

    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'stark = sc3dg.cli:cli',
        ]}
)
