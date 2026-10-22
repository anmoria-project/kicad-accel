if [ ! -d .venv ]; then
	python3 -m venv .venv
	python -m pip install --upgrade pip
	pip install kiutils
fi
source .venv/bin/activate
## NOTE: Not working. Add a .sh script that executes the python script...
# export PATH=$PATH:${PWD}

