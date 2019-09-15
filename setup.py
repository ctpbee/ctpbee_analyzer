import setuptools
import codecs
import os


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()


setuptools.setup(
    name="ctpbee_analyzer",
    version="0.0.3",
    author="faithforus",
    author_email="ljunf817@163.com",
    description="ctpbee_analyzer",
    # long_description=read('README.rst'),
    keywords="python package ctpbee",
    url="https://github.com/ctpbee/ctpbee_analyzer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
