from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from otel_trace_sender import build_zipkin_spans, post_with_retry


PORT = int(os.environ.get("PORT", "8089"))
JAEGER_ZIPKIN_URL = os.environ.get("JAEGER_ZIPKIN_URL", "http://localhost:9411/api/v2/spans")
ROOT = Path(__file__).resolve().parents[1]
TRACE_FILE = ROOT / "traces" / "public_runs.jsonl"


def _raw_public_traces() -> list[dict[str, object]]:
    return [json.loads(line) for line in TRACE_FILE.read_text().splitlines() if line.strip()]


class Handler(BaseHTTPRequestHandler):
    def _json(self, status: int, payload: object) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/healthz":
            self._json(200, {"ok": True})
            return
        if self.path == "/traces/public":
            self.send_response(200)
            self.send_header("content-type", "application/x-ndjson")
            self.end_headers()
            self.wfile.write(TRACE_FILE.read_bytes())
            return
        self._json(404, {"error": "not_found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path == "/emit/public":
            try:
                spans = build_zipkin_spans(_raw_public_traces())
                post_with_retry(JAEGER_ZIPKIN_URL, spans)
            except Exception as exc:  # pragma: no cover - exercised by Docker integration failures
                self._json(503, {"error": str(exc)})
                return
            self._json(200, {"ok": True, "emitted_spans": len(spans), "jaeger_post_success": True})
            return
        self._json(404, {"error": "not_found"})

    def log_message(self, format: str, *args: object) -> None:
        return


if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    print(f"trace simulator listening on {PORT}")
    server.serve_forever()
