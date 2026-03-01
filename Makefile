export UV_PYTHON_PREFERENCE := system

export VIRTUAL_ENV = .venv
venv_bin := $(VIRTUAL_ENV)/bin

lock_file ?= requirements.lock.txt

uv ?= uv
ifeq ($(UV_QUIET), 1)
uv += -q
endif

.PHONY: venv deps test run notebook lock-deps

venv:
	$(uv) venv --allow-existing $(VIRTUAL_ENV)

lock-deps: venv
	$(uv) pip compile --universal --no-header requirements.in -o $(lock_file)

deps: venv
	$(uv) pip sync -C editable_mode=compat $(lock_file)
	$(uv) pip install --no-deps -e postseason_simulator

test: deps
	$(venv_bin)/pytest postseason_simulator/tests -s

run: deps
	$(venv_bin)/python run.py

notebook: deps
	$(venv_bin)/jupyter notebook analysis/