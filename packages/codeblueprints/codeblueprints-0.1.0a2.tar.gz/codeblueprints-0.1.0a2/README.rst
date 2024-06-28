==============
codeblueprints
==============

Automates code planning by mapping issues(softwares requirements) to actionable modifications in your codebase, preparing for future code generation.

* Free software: Apache Software License 2.0


Features
--------

* TODO

Setup Dev
---------
Install dependency:
$ poetry lock
$ poetry install --no-root
$ poetry install --no-root --with dev

Publish to pypi:
$ rm -rf dist
$ poetry build
$ twine check dist/*
$ twine upload dist/*

需要用这个命令来确保requirement发生改变
$ poetry export --with dev -f requirements.txt --without-hashes --output requirements-dev.txt
