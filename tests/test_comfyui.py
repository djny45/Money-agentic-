from unittest.mock import patch

from app.comfyui import ComfyUIClient


def test_comfyui_queue_workflow():
    client = ComfyUIClient()
    workflow = {"1": {"class_type": "SaveImage", "inputs": {}}}
    with patch("urllib.request.urlopen") as open_url:
        open_url.return_value.__enter__.return_value.read.return_value = b'{"prompt_id":"abc"}'
        result = client.queue_workflow(workflow, client_id="test-client")
    assert result["prompt_id"] == "abc"
    request = open_url.call_args.args[0]
    assert request.full_url.endswith("/prompt")
