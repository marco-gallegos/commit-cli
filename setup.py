"""
@Author Marco A. Gallegos
@Date   2020/12/31
@update 2021/01/18
@Description
    archivo que describe el paquete distribuible
"""
import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="commitcli",
    version="1.1.0",
    author="Marco A. Gallegos",
    author_email="ma_galeza@hotmail.com",
    description="commit cli for git with some formats, by default short version of odoo format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marco-gallegos/commit-cli",
    license="MIT",
    keywords = "cli, ",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'inquirer',
        'click'
    ],
    # hacer que setup tools genere un comando cli
    entry_points={
        'console_scripts': ['commitcli=commitcli.commitcli:main'],
    }
)