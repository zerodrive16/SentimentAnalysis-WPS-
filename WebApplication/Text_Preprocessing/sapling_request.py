import requests
from pprint import pprint

try:
    response = requests.post(
        "https://api.sapling.ai/api/v1/edits",
        json={
            "key": "433NFT4SZ90NHDXO24EC0E1V9BI0ND11",
            "text": "What is thiss port.",
            "session_id": "test.py session",
            "auto_apply": True
        }
    )
    resp_json = response.json()
    if 200 <= response.status_code < 300:
        edits = resp_json['edits'] # Entire JSON
        correctedText = resp_json["applied_text"] # Full text
        pprint(edits)
        pprint(correctedText)
    else:
        print("Error: ", resp_json)
except Exception as e:
    print("Error: ", e)