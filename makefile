build:
	python setup.py sdist bdist_wheel

upload-pypi:
	python -m twine upload --repository-url dist/*

upload-test:
	python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

clean:
	rm -rf dist/*
	rm -rf build/*

test:
	python -m pytest

test-install:
	python -m venv ~/test-venv && ~/test-venv/bin/python -m pip install jsonapi-simple && ~/test-venv/bin/python -c "import jsonapi; print(jsonapi.__version__)" && rm -rf ~/test-venv
