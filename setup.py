"""
@author Marco A. Gallegos
@date 2020/03/10
@description
    archivo que describe el paquete distribuible
"""
import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="commitcli",
    version="0.0.1",
    author="Marco A. Gallegos",
    author_email="ma_galeza@hotmail.com",
    description="commit cli for git with some formats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marco-gallegos/commit-cli",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'inquirer',
        'peewee'
    ],
    # hacer que setup tools genere un comando cli
    entry_points={
        'console_scripts': ['commitcli=commitcli.commitcli:main'],
    }
)