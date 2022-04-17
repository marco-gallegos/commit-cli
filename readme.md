# Git Commmit Cli

This project provides a cli to make git commits with a minimized [odoo format](https://www.odoo.com/documentation/14.0/reference/guidelines.html#git) from a text wizard.

Is a wrapper of the `git commit -m` command writed with 💟 on Python.

This was tested on a raspbian and a fedora OS with the nano, nvim and vim editor.

supported formats:

- short odoo
- conventional commits
- free (this is like use native `git commit` command)

## Features

### Commitcli configuration file per project

You can add a `.commitclirc` file in your project directory.

you can copy the global `.commitclirc` file to your project directory and edit it to use a diferent format.

```shell
cp ~/.commitclirc .commitclirc
```

## Installation

#### 1 - Install the package

note : use sudo if the local (user) python bin dir is not in the path

```shell
sudo pip install commitcli
```

example content of the `.commitclirc` file:
```shell
#Format for every commit
#supported formats free, odoo, sgc(semantic git commits) and cc (conventional commits)
format=odoo

#Option to sign the commits o every commit, must be True or False
signgpg=False
```

change this to use cc on your project:
```shell
#Format for every commit
#supported formats free, odoo, sgc(semantic git commits) and cc (conventional commits)
format=cc

#Option to sign the commits o every commit, must be True or False
signgpg=False
```

save this file and add to your git repository and every comand will use cc format on this project.

#### 2 - Enjoy

Add files to commit

```shell
git add .
```


Use the tool

```shell
commitcli
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
- [ ] dont ask about optionals
- [ ] only make a echo of a format
- [ ] cli inline option to specify format (oddo, sgc, etc)
- [ ] module list to chose for context in cc or something like this `type(context)`
- [ ] quick templates
  - clean up
- [ ] smarter
  - store module list and provide a list of modules to choose from and the last by default
- [ ] create branches
  - use format <username>/<type "ej fix">/<free name> 

#### Formats

- [x]  conventional commits [CC](https://www.conventionalcommits.org/en/v1.0.0/)
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