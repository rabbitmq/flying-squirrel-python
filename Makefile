
run: venv/.ok
	(cd django_examples; PYTHONPATH=.. ./manage.py runserver 0.0.0.0:8000;)


venv/.ok:
	virtualenv venv
	./venv/bin/easy_install django
	rm -f distribute-0.6.10.tar.gz
	touch venv/.ok

distclean::
	rm -rf venv

clean::
	find . -name \*pyc|xargs --no-run-if-empty rm
