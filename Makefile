.PHONY: validate interop trend compact drift-check

PYTHON ?= python3
OWNERS := $(shell find profiles -mindepth 1 -maxdepth 1 -type d ! -name '.*' -exec basename {} \;)
INTEROP_ARTIFACTS := $(addsuffix /interop.v1.json,$(addprefix profiles/,$(OWNERS)))
COMPACT_ARTIFACTS := $(addsuffix /context.compact.json,$(addprefix profiles/,$(OWNERS)))

validate:
	$(PYTHON) -c "import pathlib; files=[]; [files.extend(sorted(pathlib.Path('.').glob(pattern))) for pattern in ('scripts/*.py', 'tests/test_*.py')]; [compile(path.read_text(encoding='utf-8'), str(path), 'exec') for path in files]"
	$(PYTHON) -m unittest discover -s tests -p "test_*.py"
	bash -n scripts/run_integration_hook.sh
	$(PYTHON) scripts/check_publish_guard.py --all-tracked
	$(PYTHON) scripts/validate_profile.py --allow-stale --check-raw-tracked
	$(MAKE) interop
	$(MAKE) compact
	$(MAKE) trend

interop:
	@for owner in $(OWNERS); do \
		echo "==> export interop for $$owner"; \
		$(PYTHON) scripts/export_interop_v1.py --owner-id "$$owner"; \
		$(PYTHON) scripts/validate_interop_v1.py --owner-id "$$owner"; \
	done

trend:
	$(PYTHON) scripts/benchmark_trend_report.py

compact:
	@for owner in $(OWNERS); do \
		echo "==> export compact context for $$owner"; \
		$(PYTHON) scripts/export_context_compact.py --owner-id "$$owner"; \
		$(PYTHON) scripts/validate_context_compact.py --owner-id "$$owner"; \
	done

drift-check:
	git diff --exit-code -- $(INTEROP_ARTIFACTS) $(COMPACT_ARTIFACTS) benchmarks/runs/trends.json benchmarks/runs/trends.md
