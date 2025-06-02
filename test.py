
import requests

# Replace with your actual API key
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6IjdjNTQ2NWRiLTZhNmEtNDA3ZS1hNDE4LTFkOGIxMGJhM2ExYiIsIm9yZ0lkIjoiNDUwMjY0IiwidXNlcklkIjoiNDYzMjgzIiwidHlwZUlkIjoiYzcyY2RmOTMtZDFiYy00MTU1LTk1MTgtZjUzN2I1NGI1NzY5IiwidHlwZSI6IlBST0pFQ1QiLCJpYXQiOjE3NDg3MjI4NzAsImV4cCI6NDkwNDQ4Mjg3MH0.tFRMioogXvr6sox4O__ufbiWBqnnRitIA7-o-FaWF_k"

# NFT details
contract_address = "0x524cab2ec69124574082676e6f654a18df49a048"
token_id = "7603"

# Moralis API URL
url = f"https://deep-index.moralis.io/api/v2.2/nft/{contract_address}/{token_id}"

# Request headers
headers = {
    "accept": "application/json",
    "X-API-Key": API_KEY
}

# Send GET request
response = requests.get(url, headers=headers)

# Output result
if response.status_code == 200:
    data = response.json()
    print("✅ NFT Metadata:")
    print(f"Name: {data.get('name')}")
    print(f"Token ID: {data.get('token_id')}")
    # print(f"Image: {data.get('metadata', {}).get('image')}")
    print(f"Full JSON:\n{data}")
else:
    print(f"❌ Error {response.status_code}: {response.text}")
