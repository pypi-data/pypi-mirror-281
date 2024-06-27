import os
import shutil
import subprocess
from setuptools import setup, find_packages


setup(
    name = "dung_pt",
    version = "1.0",
    author = "VuDung",
    author_email = "vuhuudung@gmail.com",
    description = "thu vien dung_pt",
    long_description = open("README.md", "r", encoding="utf-8").read(),
    long_description_content_tpye = "text/markdown",
    #url = ''
    classifiers=[
        "programing Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Independent"
    ],
    python_requires=">=3.7", #phiên bản python
    packages=find_packages(), #tìm kiếm các gói
    install_requires=[
        "requests",
        "pandas",
        "openpyxl"
    ],
    keywords = ["dung_pt", "python"],
    setup_requires=[
        "setuptools>=42",
        "wheel"
    ],
)