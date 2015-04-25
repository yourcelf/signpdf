import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="signpdf",
    version="0.0.3",
    author="Charlie DeTar",
    author_email="cfd@media.mit.edu",
    url="https://github.com/yourcelf/signpdf",
    description=("Utility for adding signatures images to PDF documents"),
    long_description=read('README.md'),
    license="MIT",
    py_modules=['signpdf'],
    entry_points={'console_scripts': ['signpdf = signpdf:main']},
    install_requires=['reportlab', 'pypdf2'],
    include_package_data=True
)


    

