"""
@Author Marco A. Gallegos
@Date   2020/12/31
@update 2022/04/04
@Description
    archivo que describe el paquete distribuible.
    how to use:
    compile ->  python3 setup.py sdist bdist_wheel
"""
# TODO: this is deprecated, use pyproject instead

import setuptools

setuptools.setup(
    name="commitcli",
    version="1.5.5",
    author="Marco A. Gallegos",
    author_email="ma_galeza@hotmail.com",
    description="commit cli for git with some formats, by default conventional commits",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    url="https://github.com/marco-gallegos/commit-cli",
    license="MIT", # TODO: deprecated
    keywords="cli,cc,commit,git,odoo,github,gitlab,bitbucket,conventional commits, semantic commits",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
    #TODO: this is deprecated, use pyproject instead just works using makefile not uv
    install_requires=[
        'inquirer',
        'click',
        'loguru',
        'pendulum',
        'pygit2',
        'pymongo',
        'python-dotenv',
    ],
    # hacer que setup tools genere un comando cli -> deprecated use pyproject instead
    entry_points={
        'console_scripts': ['commitcli=commitcli.commitcli:main'],
    },

    ## test this new code
    # package_data={'': ['commitclirc']}, # just to add this template file and us it instead hardcoding it
    # include_package_data=True,
)
