.PHONY: build clean_build upload help default

# NOTE: defaut parameters value
SCRIPT := runcommitcli.py

default: build

help:
	@echo "Usage: make [build|clean_build|upload]"
	@echo "build: Compiles the package in pip package format"
	@echo "clean_build: Cleans the build directory"
	@echo "upload: Uploads the package to PyPI"
	@echo "watch: Watches a script file for changes and executes it"

build:
	@echo "Compiling..."
	@python3 setup.py sdist bdist_wheel
	@echo "Done"

clean_build:
	@echo "Cleaning..."
	@rm -rf build dist
	@echo "Done"

upload:
	@twine upload dist/*

installdevtools:
	@pip3 install twine -U
	@npm i -g nodemon

watch:
	@if [ -z "$(SCRIPT)" ]; then \
		echo "Please specify a script file to watch using the SCRIPT parameter. Example: make watch SCRIPT=myscript.py"; \
	else \
		echo "Watching $(SCRIPT) for changes..."; \
		nodemon --watch . --ext py --exec "clear && echo 'Executing $(SCRIPT)...' && python3 $(SCRIPT)"; \
	fi


