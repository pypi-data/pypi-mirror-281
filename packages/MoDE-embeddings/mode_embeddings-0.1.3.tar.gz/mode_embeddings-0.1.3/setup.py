"""Setup."""

from setuptools import find_packages, setup, Extension
from Cython.Build import cythonize
import numpy
import os

sourcefiles = [
    "src/MoDE_embeddings/fast_mat_mul/fastgd/bootstrap.c",
    "src/MoDE_embeddings/fast_mat_mul/fastgd/fastgd_base.c",
    "src/MoDE_embeddings/fast_mat_mul/fastgd/fastgd_faster.c",
    "src/MoDE_embeddings/fast_mat_mul/fastgd/fastgd_cython.c"
]
exts = Extension(
            name="MoDE_embeddings.fast_mat_mul.fastgd",
            sources = sourcefiles,
            include_dirs=[numpy.get_include()]
    )

c_exts = cythonize([exts])

setup(
    name="MoDE_embeddings",
    version="0.1.3",
    packages=find_packages(where="src"),
    package_dir={'': 'src'},
    package_data={'MoDE_embeddings.fast_mat_mul.fastgd': [
        '*.pyx',
        '*.pxd'
    ]},
    ext_modules=c_exts,
)