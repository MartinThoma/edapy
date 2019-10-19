upload:
	make clean
	python3 setup.py sdist bdist_wheel && twine upload dist/*
clean:
	python setup.py clean --all
	pyclean .
	rm -rf *.pyc __pycache__ build dist edapy.egg-info tests/reports tests/__pycache__ edapy/csv/__pycache__ edapy/__pycache__ edapy/images/__pycache__
muation-test:
	mutmut run
