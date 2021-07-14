default:
	python3 main.py

venv:
	python3 -m venv venv
	source ./venv/bin/activate

setup: install_requirements generateconfig generatetables

install_requirements:
	pip3 install -r requirements.txt

generateconfig:
	python3 genconfig.py

generatetables:
	python3 gentables.py

run: default