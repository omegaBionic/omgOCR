from setuptools import setup, Extension
from Cython.Build import cythonize


module = [Extension('core', ['./src/core.py'],)]

setup(
    name='omgOcr',
    version='V1.0',
    requires=["setuptools", "wheel", "Cython", "re", "glob", "os", "sys", "cv2", "imutils", "numpy", "pytesseract"],
    url='',
    license='Open Source',
    author='',
    author_email='',
    description='OCR',
    build_ext='bin',
    ext_modules=cythonize('./src/*.py')
)
