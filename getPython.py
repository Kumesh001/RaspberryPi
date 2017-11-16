import requests
import json
r=requests.get("https://ub4qge1nh1.execute-api.us-west-2.amazonaws.com/prod/TriggerFunction")

print(r.status_code)
print(r.headers)
print(r.content)
