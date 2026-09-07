# Releases

## 0.5.1 — legacy privacy policy compatibility

- Automatically normalize the old list-based policy format during validation and compact/MCP export.
- Preserve explicit restrictions and the original file; unlisted fields default to local-only.
- Reject mixed formats, conflicting rules, malformed JSON and owner mismatches with actionable errors.
- No manual schema rewrite is required for supported legacy policies.


## 0.5.0 — portable onboarding and tested integrations

- Ship templates, schemas and the hook script in the installable package.
- Make owner alias optional and allow minimal-only interop/compact export.
- Keep new profiles provisional; preflight all starter files before writing and reject unsafe owner paths.
- Require valid matching policies for compact/MCP exports, with explicit `--allow-unfiltered` for missing-policy legacy use.
- Add an installed SET adapter and owner-local bootstrap path checks, tested with agentsgen 0.5.0 and SET 0.3.1.
- Replace live-metrics marketing with a dated reproducible benchmark snapshot and three synthetic release demos.
- Verify source, installed wheel, privacy behavior and interoperability before publication.

Upgrade: `uv tool upgrade id-protocol` or `pipx upgrade id-protocol`.
Existing core/extended profiles remain supported. Version 0.5.1 adds automatic compatibility for the legacy list format. Other invalid
policies still require review.
This release does not update the owner's review dates or infer new personal facts.

MCP export is a resource payload, not a server. Release automation no longer registers
this CLI as an executable MCP server. Older registry entries do not establish runtime support.

## Release procedure

Run `make validate`, `make drift-check`, and `make coverage`; build and check the wheel.
Run the installed-package demos and the pinned SET Action integration. Merge only after CI.
Tag the reviewed version. Verify GitHub assets, PyPI publication and a fresh public-index install.

Checked-in benchmark reports use `benchmarks/reference-date.txt`; update that explicit
snapshot date when refreshing reports. Live profile validation continues to use today's date.

Earlier releases: [GitHub history](https://github.com/markoblogo/ID/releases).
