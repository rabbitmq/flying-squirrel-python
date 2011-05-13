
build:
	python setup.py build

test: tests
tests:
	SERVICE_URL='http://guest:guest@localhost:55672/socks-api/default' \
		python setup.py test

clean::
	rm -rf flyingsquirrel.egg-info build
	find . -name \*pyc|xargs --no-run-if-empty rm
