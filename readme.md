# Git Commmit Cli

This project provides a cli to make git commits with a minimized [odoo format](https://www.odoo.com/documentation/14.0/reference/guidelines.html#git) from a text wizard.

Is a wrapper of the `git commit -m` command writed with 💟 on Python.

This was tested on a raspbian and a fedora OS with the nvim and vim editor

## Instalation

#### 1 - Install the package

note : use sudo if the local (user) python bin dir is not in the path

```shell
sudo pip install commitcli
```

#### 2 - Enjoy

Add files to commit

```shell
git add .
```


Use the tool

```shell
comitcli
```


## Next Updates

#### Formats

- [ ]  semantic git commit [SGC](https://www.npmjs.com/package/semantic-git-commit-cli)
- [ ]  full odoo tags


## Development


## Help

using without install from the source 

python -m commitcli


and defining the __main__.py file


## References

https://magmax.org/python-inquirer/

https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html

https://setuptools.readthedocs.io/en/latest/userguide/entry_point.html

https://medium.com/better-programming/python-click-building-your-first-command-line-interface-application-6947d5319ef7