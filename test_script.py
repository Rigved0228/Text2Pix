import requests

# Replace YOUR_TOKEN_HERE with your token (keep the hf_ prefix)
# e.g., "hf_abcdefghijklmnopqrstuvwxyz"
token = "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"

headers = {"Authorization": f"Bearer {token}"}
response = requests.get("https://huggingface.co/api/whoami", headers=headers)
print(f"Status code: {response.status_code}")
print(f"Response: {response.text}")
