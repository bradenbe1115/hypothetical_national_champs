export UV_PYTHON_PREFERENCE := system

export VIRTUAL_ENV = .venv
venv_bin := $(VIRTUAL_ENV)/bin


uv ?= uv
ifeq ($(UV_QUIET), 1)
uv += -q
endif

lock_file ?= requirements.lock.txt
spider_name ?= 

venv: 
	$(uv) venv --allow-existing $(VIRTUAL_ENV)

lock-deps: venv
	$(uv) pip compile --universal --no-header requirements.in -o $(lock_file)

deps: venv
	$(uv) pip sync -C editable_mode=compat $(lock_file)

test: deps
	$(venv_bin)/pytest -s .

job_name ?=

run_ingest_ratings_api: deps
	$(venv_bin)/python -m ingest_college_football_ratings_api $(job_name)
