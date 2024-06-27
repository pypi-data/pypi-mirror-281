import os
import glob
import numpy as np

from setuptools import setup, find_packages
from setuptools.extension import Extension

try:
    from Cython.Build import cythonize
    HAVE_CYTHON = True
except ImportError:
    HAVE_CYTHON = False

numpy_includes = np.get_include()

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

def get_ext_modules():
    extensions = []
    
    # Add parse_pysam.pyx to the extensions
    parse_pysam_path = os.path.join("sc3dg", "pairtools", "lib", "parse_pysam.pyx")
    if os.path.exists(parse_pysam_path):
        import pysam
        extensions.append(
            Extension(
                "sc3dg.pairtools.lib.parse_pysam",
                [parse_pysam_path],
                extra_link_args=pysam.get_libraries(),
                include_dirs=pysam.get_include() + [numpy_includes],
                define_macros=pysam.get_defines(),
                language="c",
            )
        )
    
    # Add other extensions
    ext = ".pyx" if HAVE_CYTHON else ".c"
    src_files = glob.glob(
        os.path.join(os.path.dirname(__file__), "sc3dg", "pairtools", "lib", "*" + ext)
    )

    for src_file in src_files:
        name = "sc3dg.pairtools.lib." + os.path.splitext(os.path.basename(src_file))[0]
        if "pysam" not in name and "regions" not in name and name != "sc3dg.pairtools.lib.parse_pysam":
            extensions.append(Extension(name, [src_file], include_dirs=[numpy_includes]))
        elif "regions" in name:
            extensions.append(
                Extension(
                    name,
                    [src_file],
                    language="c++",
                    include_dirs=[numpy_includes],
                )
            )

    if HAVE_CYTHON:
        extensions = cythonize(extensions, language_level="3")

    return extensions

setup(
    name="sc3dg",
    version="0.0.44",
    description="A toolkit for processing single cell Hi-C data",
    author="Your Name",  # Replace with actual author name
    author_email="your.email@example.com",  # Add author email
    ext_modules=[
        Extension("sc3dg.model.dyn_util", ["sc3dg/model/dyn_util.c"],
                  libraries=["m"],
                  include_dirs=[numpy_includes])
    ] + get_ext_modules(),
    packages=find_packages(),
    install_requires=install_requires,
    setup_requires=['numpy'],  # Add numpy to setup_requires
    entry_points={
        'console_scripts': [
            'stark = sc3dg.cli:cli',
            'pairtools = sc3dg.pairtools.cli:cli',
        ]
    },

   
)
