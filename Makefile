install:
	poetry install
test:
	poetry run pytest
lint:
	poetry run flake8 gendiff
build:
	poetry build
clean-build:
	rm -rf dist
publish:
	poetry publish --dry-run
publish-testpypi:
	poetry config repositories.testpypi https://test.pypi.org/legacy/
	poetry publish -r testpypi 
package-install:
	python3 -m pip install --user dist/*.whl
