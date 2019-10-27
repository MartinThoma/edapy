upload:
	make clean
	python3 setup.py sdist bdist_wheel && twine upload dist/*

clean:
	python setup.py clean --all
	pyclean .
	rm -rf *.pyc __pycache__ build dist edapy.egg-info tests/reports tests/__pycache__ edapy/csv/__pycache__ edapy/__pycache__ edapy/images/__pycache__

muation-test:
	mutmut run

mutmut-results:
	mutmut junitxml --suspicious-policy=ignore --untested-policy=ignore > mutmut-results.xml
	junit2html mutmut-results.xml mutmut-results.html

bandit:
	# Not a security application: B311 and B303 should be save
	# Python3 only: B322 is save
	bandit -r edapy #-s B311,B303,B322
