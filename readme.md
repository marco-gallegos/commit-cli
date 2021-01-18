# Git Commmit Cli

This project provides a cli to make git commits with a minimized [odoo format](https://www.odoo.com/documentation/14.0/reference/guidelines.html#git) from a text wizard.

Is a wrapper of the `git commit -m` command writed with 💟 on Python.

This was tested on a raspbian and a fedora OS with the nano, nvim and vim editor.

supported formats:

- short odoo
- conventional commits
- free (this is like use native `git commit` command)

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

### Example

#### Odoo (default)

![ejemplo de imagen](./static/img/example.png)

## Configuration

This utility creates a file into the users home directory `~/.commitclirc` in this file you will find some customizable options. the most important is the format option this option accepts this formats:

- odoo
- cc
- free


## Next Updates

#### Formats

- [*] config manager using ~/.comirclirc file
- [*]  conventional commits [CC](https://www.conventionalcommits.org/en/v1.0.0/)
  - [tags](https://github.com/conventional-changelog/commitlint/tree/master/%40commitlint/config-conventional)  
- [ ]  semantic git commit [SGC](https://www.npmjs.com/package/semantic-git-commit-cli)
- [ ]  full odoo tags
- [ ]  configuration changes using the cli


## Development


## Help

using without install from the source 

python -m commitcli


## References

https://magmax.org/python-inquirer/

https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html

https://setuptools.readthedocs.io/en/latest/userguide/entry_point.html

https://medium.com/better-programming/python-click-building-your-first-command-line-interface-application-6947d5319ef7