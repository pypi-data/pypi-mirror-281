from setuptools import setup, find_packages
import numpy as np

def read(rel_path: str) -> str:
    with open(rel_path) as fp:
        return fp.read()
        
def get_version(rel_path: str) -> str:
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")

setup(
    name='unav',
    version=get_version("unav/__init__.py"),
    author='Your Name',
    author_email='your.email@example.com',
    description='UNav is designed for helping navigation of visually impaired people',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/UNav',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['*.so'],
    },
    install_requires=[
        'numpy',
        'torch',
        'opencv-python',
        'h5py',
        'scikit-image',
        'requests'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.6',
)
