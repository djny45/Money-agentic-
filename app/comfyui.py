import json
import urllib.request
import uuid
from typing import Any


class ComfyUIClient:
    """Minimal client for a local/self-hosted ComfyUI server.

    ComfyUI is open source. This client submits API-format workflows to the
    local server and never requires a hosted image-generation API key.
    """

    def __init__(self, base_url: str = "http://127.0.0.1:8188", timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def health(self) -> dict[str, Any]:
        request = urllib.request.Request(f"{self.base_url}/system_stats")
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                return {"ok": True, "status": response.status, "data": json.loads(response.read())}
        except Exception as exc:
            return {"ok": False, "error": str(exc)}

    def queue_workflow(self, workflow: dict[str, Any], client_id: str | None = None) -> dict[str, Any]:
        payload: dict[str, Any] = {"prompt": workflow, "client_id": client_id or str(uuid.uuid4())}
        data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            f"{self.base_url}/prompt",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=self.timeout) as response:
            return json.loads(response.read())

    def history(self, prompt_id: str) -> dict[str, Any]:
        request = urllib.request.Request(f"{self.base_url}/history/{prompt_id}")
        with urllib.request.urlopen(request, timeout=self.timeout) as response:
            return json.loads(response.read())
