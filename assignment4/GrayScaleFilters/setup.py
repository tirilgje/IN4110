import cv2
import numpy as np
from distutils.core import setup
from Cython.Build import cythonize

setup(
    name='Cython modules',
    ext_modules=cythonize("*.pyx"),
)
      #include_dirs=[numpy.get_include()])