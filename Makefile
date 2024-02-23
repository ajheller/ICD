.PHONY: help create-env start-server generate-api

help:
	echo HI

create-env:
	micromamba create -n ICD python=3.10
	micromamba run -n ICD pip install fabric zeroapi ipython jupyterlab 

start-server:
	micromamba run -n ICD python -m server

generate-api:
	micromamba run -n ICD python -m zero.generate_client --host localhost --port 5559 --overwrite-dir ./my_client
