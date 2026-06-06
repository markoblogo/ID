from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any, Iterator
from unittest.mock import patch

import scripts.publish_mcp_manifest as manifest_script


@contextlib.contextmanager
def _start_capture_server(captured: dict[str, Any]) -> Iterator[str]:
    class CaptureHandler(BaseHTTPRequestHandler):
        def do_POST(self) -> None:  # noqa: N802 (stdlib method signature)
            length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(length)
            if body:
                captured["payload"] = json.loads(body.decode("utf-8"))
            captured["path"] = self.path
            captured["method"] = self.command
            captured["authorization"] = self.headers.get("Authorization")
            self.send_response(201)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True}).encode("utf-8"))

        def log_message(self, _format: str, *args: object) -> None:  # noqa: ARG002
            return

    server = HTTPServer(("127.0.0.1", 0), CaptureHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=1)


class PublishMcpManifestTests(unittest.TestCase):
    def test_skip_without_endpoint(self) -> None:
        with (
            tempfile.TemporaryDirectory(),
            patch.dict(manifest_script.os.environ, {"MCP_REGISTRY_ENDPOINT": ""}, clear=False),
            contextlib.redirect_stdout(io.StringIO()),
            patch.object(sys, "argv", ["publish-mcp-manifest.py"]),
        ):
            self.assertFalse(manifest_script.parse_args().endpoint)
            self.assertEqual(manifest_script.main(), 0)

    def test_dry_run_prints_payload(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest = Path(tmp) / "mcp-manifest.json"
            manifest.write_text(
                json.dumps({"name": "ID", "version": "0.2.3"}),
                encoding="utf-8",
            )
            with patch.object(
                sys,
                "argv",
                [
                    "publish-mcp-manifest.py",
                    "--manifest",
                    str(manifest),
                    "--endpoint",
                    "https://example.com/manifests",
                    "--dry-run",
                    "--version",
                    "0.2.3",
                ],
            ):
                args = manifest_script.parse_args()
            payload = manifest_script.build_payload(manifest_script.load_manifest(manifest), args)
            self.assertIn("manifest", payload)
            self.assertEqual(payload["registry_project"], "markoblogo/ID")
            self.assertIn("version", payload)
            self.assertEqual(payload["version"], "0.2.3")

    def test_publish_posts_payload(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest = Path(tmp) / "mcp-manifest.json"
            manifest.write_text(
                json.dumps({"name": "ID", "version": "0.2.3"}),
                encoding="utf-8",
            )
            manifest_data = manifest_script.load_manifest(manifest)
            with patch.object(sys, "argv", ["publish-mcp-manifest.py", "--manifest", str(manifest)]):
                args = manifest_script.parse_args()
            payload = manifest_script.build_payload(manifest_data, args)
            captured: dict[str, Any] = {}

            with _start_capture_server(captured) as endpoint:
                with contextlib.redirect_stdout(io.StringIO()):
                    manifest_script.publish(payload, endpoint + "/manifests", None, timeout=5.0)

            self.assertEqual(captured["method"], "POST")
            self.assertEqual(captured["path"], "/manifests")
            self.assertIsInstance(captured["payload"], dict)
            self.assertEqual(captured["payload"]["registry_project"], "markoblogo/ID")
            self.assertEqual(captured["payload"]["manifest"]["name"], "ID")

    def test_publish_passes_authorization_header(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest = Path(tmp) / "mcp-manifest.json"
            manifest.write_text("{}", encoding="utf-8")
            manifest_data = manifest_script.load_manifest(manifest)
            with patch.object(sys, "argv", ["publish-mcp-manifest.py", "--manifest", str(manifest)]):
                args = manifest_script.parse_args()
            payload = manifest_script.build_payload(manifest_data, args)
            captured: dict[str, Any] = {}

            with _start_capture_server(captured) as endpoint:
                with contextlib.redirect_stdout(io.StringIO()):
                    manifest_script.publish(payload, endpoint + "/manifests", "abc123", timeout=5.0)

            self.assertEqual(captured["authorization"], "Bearer abc123")


if __name__ == "__main__":
    unittest.main()
