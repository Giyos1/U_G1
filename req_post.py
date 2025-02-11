import requests

url = 'http://127.0.0.1:8000/book/create/'

data = {
    "title": "Alo",
    "author": 2
}

response = requests.post(url, json=data)
print(response.status_code)
