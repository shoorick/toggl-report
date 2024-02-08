.PHONY: prepare test clean

prepare venv: requirements.txt
	( \
		python3 -m venv venv; \
		. venv/bin/activate; \
		pip install -r requirements.txt; \
	)

test: venv
	( \
		. venv/bin/activate; \
		pytest; \
	)

clean:
	find . -type f -name \*.pyc -delete
	find . -type d -name __pycache__ -delete
	rm -r .pytest_cache
