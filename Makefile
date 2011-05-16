PYTHON=./venv/bin/python


.PHONY: all
all: venv/.ok sdist tests

venv:
	mkdir venv

# For python2.6 we need unittest backported from 2.7.
venv/.ok: venv
	virtualenv venv
	./venv/bin/pip install unittest2
	touch venv/.ok
	rm -f distribute-0.6.10.tar.gz

# The tests expect a running Flying Squirrel service.
.PHONY: test tests
test: tests
tests:
	SERVICE_URL='http://guest:guest@localhost:55672/socks-api/default' \
		${PYTHON} setup.py test

.PHONY: sdist
sdist:
	python setup.py sdist


.PHONY: clean
clean::
	rm -rf flyingsquirrel.egg-info build dist venv distribute-0.6.10.tar.gz
	find . -name \*pyc|xargs --no-run-if-empty rm
