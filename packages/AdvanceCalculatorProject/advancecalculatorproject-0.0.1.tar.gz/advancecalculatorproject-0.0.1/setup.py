from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Simple advance calculator '
LONG_DESCRIPTION = 'A package that allows to perfoming simple calculus integrals and derivative, ploting any type of graph as well as solving simple cuadratic equations with the help of Numpy and Simpy packages'

# Setting up
setup(
    name="AdvanceCalculatorProject",
    version=VERSION,
    author="Napain (Simon Torrealba)",
    author_email="storrealba24@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['simpy','numpy'],
    keywords=['python', 'calculus', 'ploting', 'solver', 'calculator']

)