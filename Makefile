.PHONY: check validate test example

check: validate test example

validate:
	python3 commands/validate.py

test:
	python3 -m unittest discover -s tests -v

example:
	python3 examples/stale-handoff/demo.py
