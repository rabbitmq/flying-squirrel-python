
# The tests expect a running Flying Squirrel service.
test: tests
tests:
	SERVICE_URL='http://guest:guest@localhost:55672/socks-api/default' \
		python setup.py test

sdist:
	python setup.py sdist


clean::
	rm -rf flyingsquirrel.egg-info build dist
	find . -name \*pyc|xargs --no-run-if-empty rm
