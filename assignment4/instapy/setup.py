import numpy
import setuptools
from setuptools.extension import Extension
from Cython.Build import cythonize


extensions=[
    Extension("cython_color2gray", ["instapy/_cython_grayscale.pyx"],
    include_dirs=[numpy.get_include()],
    ), Extension("cython_color2sepia", ["instapy/_cython_sepia.pyx"],
    include_dirs=[numpy.get_include()])
]

setuptools.setup(
    name="instapy",
    version="0.0.13",
    author="Tiril Gjerstad",
    author_email="tirilagj@uio.no",
    description="Instagram filters in Python",
    #long_description=long_description,
    #long_description_content_type="text/markdown",
    #url="https://github.uio.no/IN3110/IN3110-vegarvi/",
    packages=setuptools.find_packages(),
    scripts=["bin/instapy"],
    ext_modules=cythonize(extensions),
    setup_requires=["cython", "numpy", "setuptools>=18.0"],
    install_requires=["numpy", "numba", "opencv-python"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)