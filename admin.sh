#!/bin/bash
: '
This file has some functions to help you with the administration of the package.

pip install twine
'

if [[ $1 ]]; then
	case $1 in
		"build" )
      echo "Compiling..."
      python3 setup.py sdist bdist_wheel
      echo "Done"
		;;

		"upload" )
		  twine upload dist/*
		;;

    "--help" )
      echo "Usage: ./admin.sh [build|upload]"
      echo "build: Compiles the package in pip package format"
      echo "upload: Uploads the package to PyPi"
    ;;

		*)
			echo "invalid option: $1"
	esac
fi