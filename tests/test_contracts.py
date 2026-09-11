from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = REPO_ROOT / "schemas"
API_DIR = REPO_ROOT / "api"


class ContractTests(unittest.TestCase):
    def test_schema_ids_use_public_raw_url(self) -> None:
        for path in SCHEMA_DIR.glob("*.json"):
            schema = json.loads(path.read_text(encoding="utf-8"))
            schema_id = schema.get("$id", "")
            self.assertTrue(
                schema_id.startswith("https://raw.githubusercontent.com/markoblogo/ID/main/schemas/"),
                path,
            )

    def test_api_contracts_exist(self) -> None:
        self.assertTrue((API_DIR / "id-protocol.openapi.yaml").exists())
        self.assertTrue((API_DIR / "id-protocol.mcp.json").exists())

    def test_mcp_contract_is_design_only(self) -> None:
        contract = json.loads((API_DIR / "id-protocol.mcp.json").read_text(encoding="utf-8"))
        self.assertEqual(contract["status"], "design-only")
        self.assertFalse(contract["runtimeIncluded"])
        self.assertIn("contractVersion", contract)
        self.assertFalse((REPO_ROOT / "mcp-manifest.json").exists())

    def test_readme_does_not_claim_an_mcp_server(self) -> None:
        readme = REPO_ROOT.joinpath("README.md").read_text(encoding="utf-8")
        self.assertIn("does not provide an MCP server", readme)


if __name__ == "__main__":
    unittest.main()
