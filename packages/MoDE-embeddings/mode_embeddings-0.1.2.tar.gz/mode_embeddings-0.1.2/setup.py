"""Setup."""

from setuptools import find_packages, setup, Extension
from Cython.Build import cythonize
import numpy
import os

# Installation
# config = {
#     'name': 'MoDE-embeddings',
#     'version': '0.1.0',
#     'packages': find_packages(),
#     'package_data': {'src.MoDE_embeddings.fast_mat_mul.fastgd': ['*.pyx', '*.pxd']},
#     'ext_modules': cythonize(["src/MoDE_embeddings/fast_mat_mul/fastgd/*.pyx"]),
#     'zip_safe': True
# }

sourcefiles = [
    "src/MoDE_embeddings/fast_mat_mul/fastgd/bootstrap.c",
    "src/MoDE_embeddings/fast_mat_mul/fastgd/fastgd_base.c",
    "src/MoDE_embeddings/fast_mat_mul/fastgd/fastgd_faster.c",
    "src/MoDE_embeddings/fast_mat_mul/fastgd/fastgd_cython.c"
]
exts = Extension(
            name="fast_gd.bootstrap",
            sources = sourcefiles,
            include_dirs=[numpy.get_include()]
    )

print(os.listdir("src/MoDE_embeddings/fast_mat_mul/fastgd"))

c_exts = cythonize(exts)

setup(
    name="MoDE_embeddings",
    version="0.1.2",
    packages=find_packages(),
    package_data={'src.MoDE_embeddings.fast_mat_mul.fastgd': ['bootstrap.pyx',
                                                        'fastgd_base.pyx',
                                                        'fastgd_faster.pyx',
                                                        'fastgd_cython.pyx']},
    ext_modules=c_exts,
)