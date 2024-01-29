.PHONY: prepare
prepare:
	# pyenv local 3.10.10

.PHONY: test
test: prepare
	pytest

.PHONY: clean
clean:
	rm -rf sparksql_jupyter.egg-info build dist

.PHONY: dist
dist: clean
	python setup.py sdist bdist_wheel

.PHONY: upload
upload: dist
	twine upload dist/*
