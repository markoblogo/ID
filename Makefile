.PHONY: validate interop trend compact mcp privacy-policy metrics metrics-readme metrics-tokenizer lint-profile lint-profile-strict observed-behavior bootstrap-owner migrate migrate-check drift-check release-build release-check coverage mcp-manifest-sync soul

PYTHON ?= python3
PROJECT_VERSION := $(shell $(PYTHON) -c "import tomllib; import pathlib; print(tomllib.loads(pathlib.Path('pyproject.toml').read_text(encoding='utf-8'))['project']['version'])")
REPO_ROOT := $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST)))))
OWNERS := $(shell \
	if test -d profiles; then \
		for owner_dir in profiles/*/; do \
			[ -f "$$owner_dir/profile.core.md" ] || [ -f "$$owner_dir/profile.extended.md" ] || [ -f "$$owner_dir/profile.minimal.md" ] || continue; \
			basename "$$owner_dir"; \
		done; \
	fi)
INTEROP_ARTIFACTS := $(addsuffix /interop.v1.json,$(addprefix profiles/,$(OWNERS)))
COMPACT_ARTIFACTS := $(addsuffix /context.compact.json,$(addprefix profiles/,$(OWNERS)))
MCP_ARTIFACTS := $(addsuffix /mcp.context.resource.json,$(addprefix profiles/,$(OWNERS)))
PUBLIC_METRICS_ARTIFACTS := benchmarks/runs/public-metrics.json benchmarks/runs/public-metrics.md

validate:
	$(PYTHON) -c "import pathlib; files=[]; [files.extend(sorted(pathlib.Path('.').glob(pattern))) for pattern in ('scripts/*.py', 'tests/test_*.py')]; [compile(path.read_text(encoding='utf-8'), str(path), 'exec') for path in files]"
	$(PYTHON) -m unittest discover -s tests -p "test_*.py"
	bash -n scripts/run_integration_hook.sh
	$(PYTHON) scripts/check_publish_guard.py --all-tracked
	$(PYTHON) scripts/validate_profile.py --allow-stale --check-raw-tracked
	$(MAKE) lint-profile-strict
	$(MAKE) observed-behavior
	$(MAKE) privacy-policy
	$(MAKE) interop
	$(MAKE) compact
	$(MAKE) mcp
	$(MAKE) trend
	$(MAKE) metrics
	$(MAKE) metrics-readme

soul:
	@for owner in $(OWNERS); do \
		echo "==> refresh soul for $$owner"; \
		$(PYTHON) idcli.py refresh-soul --owner-id "$$owner"; \
	done

coverage:
	$(PYTHON) -m coverage run -m unittest discover -s tests -p "test_*.py"
	$(PYTHON) -m coverage report --fail-under=60
	$(PYTHON) -m coverage xml

interop:
	@for owner in $(OWNERS); do \
		echo "==> export interop for $$owner"; \
		$(PYTHON) scripts/export_interop_v1.py --owner-id "$$owner"; \
		$(PYTHON) scripts/validate_interop_v1.py --owner-id "$$owner"; \
	done

trend:
	$(PYTHON) scripts/benchmark_trend_report.py

metrics:
	$(PYTHON) scripts/benchmark_public_report.py

metrics-readme:
	$(PYTHON) scripts/generate_metrics_readme.py

release-build:
	rm -rf dist build *.egg-info
	$(PYTHON) -m build

release-check:
	@test -d dist || { echo "missing dist/; run make release-build"; exit 1; }
	$(PYTHON) -m twine check dist/*

metrics-tokenizer:
	@$(PYTHON) -c "import importlib.util, sys; sys.exit(0 if importlib.util.find_spec('tiktoken') else 1)" || { echo "Install hint: pip install tiktoken"; exit 1; }
	$(PYTHON) scripts/benchmark_public_report.py --tokenizer-provider tiktoken --tokenizer-encoding cl100k_base

lint-profile:
	$(PYTHON) scripts/lint_profile_quality.py

lint-profile-strict:
	$(PYTHON) scripts/lint_profile_quality.py --strict

observed-behavior:
	$(PYTHON) scripts/validate_observed_behavior.py

bootstrap-owner:
	@test -n "$(OWNER)" || { echo "usage: make bootstrap-owner OWNER=<owner-id> [OWNER_ALIAS=<alias>]"; exit 1; }
	$(PYTHON) "$(REPO_ROOT)/scripts/bootstrap_owner.py" --owner-id "$(OWNER)" $(if $(OWNER_ALIAS),--owner-alias "$(OWNER_ALIAS)",)

migrate:
	@test -n "$(OWNER_ID)" || { echo "usage: make migrate OWNER_ID=<owner-id> FROM=v0.1 TO=v0.2 [DRY_RUN=1]"; exit 1; }
	@test -n "$(FROM)" || { echo "usage: make migrate OWNER_ID=<owner-id> FROM=v0.1 TO=v0.2 [DRY_RUN=1]"; exit 1; }
	@test -n "$(TO)" || { echo "usage: make migrate OWNER_ID=<owner-id> FROM=v0.1 TO=v0.2 [DRY_RUN=1]"; exit 1; }
	$(PYTHON) scripts/migrate.py --owner-id "$(OWNER_ID)" --from "$(FROM)" --to "$(TO)" $(if $(DRY_RUN),--dry-run,)

migrate-check:
	$(PYTHON) scripts/migrate.py --owner-id "$(OWNER_ID)" --from "$(FROM)" --to "$(TO)" --dry-run --json

compact:
	@for owner in $(OWNERS); do \
		echo "==> export compact context for $$owner"; \
		$(PYTHON) scripts/export_context_compact.py --owner-id "$$owner"; \
		$(PYTHON) scripts/validate_context_compact.py --owner-id "$$owner"; \
	done

mcp:
	@for owner in $(OWNERS); do \
		echo "==> export mcp resource for $$owner"; \
		$(PYTHON) scripts/export_mcp_resource.py --owner-id "$$owner"; \
		$(PYTHON) scripts/validate_mcp_resource.py --owner-id "$$owner"; \
	done

privacy-policy:
	@for owner in $(OWNERS); do \
		test -f "profiles/$$owner/privacy-policy.v1.json" || { echo "missing privacy policy for $$owner"; exit 1; }; \
		echo "==> validate privacy policy for $$owner"; \
		$(PYTHON) scripts/validate_privacy_policy.py --owner-id "$$owner"; \
	done

drift-check:
	@for path in $(INTEROP_ARTIFACTS) $(COMPACT_ARTIFACTS) $(MCP_ARTIFACTS) $(PUBLIC_METRICS_ARTIFACTS) benchmarks/runs/trends.json benchmarks/runs/trends.md; do \
		test -f "$$path" || { echo "missing artifact: $$path"; exit 1; }; \
	done
	git diff --exit-code -- $(INTEROP_ARTIFACTS) $(COMPACT_ARTIFACTS) $(MCP_ARTIFACTS) $(PUBLIC_METRICS_ARTIFACTS) benchmarks/runs/trends.json benchmarks/runs/trends.md

mcp-manifest-sync:
	$(PYTHON) scripts/publish_mcp_manifest.py --version "$(PROJECT_VERSION)"
