"""Use the endpoint, flow ID and key from YOUR running visual tool."""
import os
import sys
import requests

def call_flow(kind, question):
    flow = os.environ["FLOW_ID"]
    base = os.environ["FLOW_BASE_URL"].rstrip("/")
    key = os.environ.get("FLOW_API_KEY", "")
    if kind == "langflow":
        url = f"{base}/api/v1/run/{flow}"
        payload = {"input_value": question, "input_type": "chat", "output_type": "chat"}
        headers = {"x-api-key": key} if key else {}
    elif kind == "flowise":
        url = f"{base}/api/v1/prediction/{flow}"
        payload = {"question": question}
        headers = {"Authorization": f"Bearer {key}"} if key else {}
    else:
        raise ValueError("Choose langflow or flowise")
    response = requests.post(url, json=payload, headers=headers, timeout=60)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python module03/call_flow.py langflow|flowise")
    print(call_flow(sys.argv[1], "Explain dictionaries in three short points."))
