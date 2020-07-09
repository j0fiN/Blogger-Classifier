
import requests

data = {

    "blogs": ["numpy"],

}
res = requests.request("POST", 'http://127.0.0.1:5000/result', json=data)
print(res.status_code)
print(res.json())
