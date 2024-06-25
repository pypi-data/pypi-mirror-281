override CONDA=$(CONDA_BASE)/bin/conda
override MAMBA=$(CONDA_BASE)/bin/mamba
override PKG=slurm_esr
SHELL := /bin/bash


# -----------------------
# Publication
# -----------------------
pkg_version:
	pip index versions syspop

build_pkg:
	rm -rf $(PKG).egg*
	rm -rf dist
	python setup.py sdist bdist_wheel
	pip install .

install_twine:
	pip install twine

upload_pkg: 
	twine upload dist/*

publish: build_pkg upload_pkg

del_pkg_tmp:
	rm -rf $(PKG).egg*
	rm -rf dist
	rm -rf .eggs
	rm -rf build