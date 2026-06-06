from __future__ import annotations

import json
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path
from unittest.mock import patch

import scripts.build_registry_server_json as registry_server_script


class BuildRegistryServerJsonTests(unittest.TestCase):
    def test_build_server_json_for_pypi(self) -> None:
        manifest = {
            "name": "ID",
            "display_name": "ID Protocol",
            "description": "Portable human-AI context protocol reference tooling.",
            "homepage": "https://github.com/markoblogo/ID",
            "repository": {
                "type": "git",
                "url": "https://github.com/markoblogo/ID",
            },
            "version": "0.2.8",
        }
        pyproject = {
            "project": {
                "name": "id-protocol",
                "version": "0.2.8",
            }
        }

        server = registry_server_script.build_server_json(manifest, pyproject, "markoblogo/ID", "v0.2.8")

        self.assertEqual(server["name"], "io.github.markoblogo/id")
        self.assertEqual(server["version"], "0.2.8")
        self.assertEqual(server["packages"][0]["registryType"], "pypi")
        self.assertEqual(server["packages"][0]["identifier"], "id-protocol")
        self.assertEqual(server["packages"][0]["transport"]["type"], "stdio")
        self.assertEqual(server["repository"], {"url": "https://github.com/markoblogo/ID", "source": "github"})

    def test_main_writes_server_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "mcp-manifest.json"
            pyproject = root / "pyproject.toml"
            output = root / "server.json"
            manifest.write_text(
                json.dumps(
                    {
                        "name": "ID",
                        "display_name": "ID Protocol",
                        "description": "Portable human-AI context protocol reference tooling.",
                        "homepage": "https://github.com/markoblogo/ID",
                        "version": "0.2.8",
                    }
                ),
                encoding="utf-8",
            )
            pyproject.write_text(
                "[project]\nname = \"id-protocol\"\nversion = \"0.2.8\"\n",
                encoding="utf-8",
            )

            with patch.object(
                sys,
                "argv",
                [
                    "build_registry_server_json.py",
                    "--manifest",
                    str(manifest),
                    "--pyproject",
                    str(pyproject),
                    "--version",
                    "v0.2.8",
                    "--output",
                    str(output),
                ],
            ):
                self.assertEqual(registry_server_script.main(), 0)

            written = json.loads(output.read_text(encoding="utf-8"))
            pyproject_data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
            self.assertEqual(written["packages"][0]["identifier"], pyproject_data["project"]["name"])
            self.assertEqual(written["version"], "0.2.8")


if __name__ == "__main__":
    unittest.main()
