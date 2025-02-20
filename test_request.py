import requests
from constants import USER_ENDPOINT

response = requests.get(f"{USER_ENDPOINT}/2")

print("Status Code: ", response.status_code)
print("Responce Json: ", response.json())