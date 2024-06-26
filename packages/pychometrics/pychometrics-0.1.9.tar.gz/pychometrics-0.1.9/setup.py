# setup.py
from setuptools import setup, find_packages

setup(
    name='pychometrics',
    version='0.1.9',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'scipy',
        'reportlab',
        'pytest',
    ],
    author='Siva Kumar',
    author_email='doctsh@gmail.com',
    description='A package to perform assessment analysis and generate reports',
    url='https://github.com/Shiva-DS24/pychometrics',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

