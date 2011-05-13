
.PHONY: all
all: sdist tests

# The tests expect a running Flying Squirrel service.
.PHONY: test tests
test: tests
tests:
	SERVICE_URL='http://guest:guest@localhost:55672/socks-api/default' \
		python setup.py test

.PHONY: sdist
sdist:
	python setup.py sdist


.PHONY: clean
clean::
	rm -rf flyingsquirrel.egg-info build dist
	find . -name \*pyc|xargs --no-run-if-empty rm
