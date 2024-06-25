
SHELL=/bin/bash

venv:  ## Set up virtual environment
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt

install: venv
	unset CONDA_PREFIX && \
	source .venv/bin/activate && maturin develop

install-release: venv
	unset CONDA_PREFIX && \
	source .venv/bin/activate && maturin develop --release

pre-commit: venv
	cargo fmt --all && cargo clippy --all-features
	.venv/bin/python -m ruff check . --fix --exit-non-zero-on-fix
	.venv/bin/python -m ruff format polars_reverse_geocode tests
	.venv/bin/python -m mypy polars_reverse_geocode tests

test: venv
	.venv/bin/python -m pytest tests

run: install
	source .venv/bin/activate

run-release: install-release
	source .venv/bin/activate
