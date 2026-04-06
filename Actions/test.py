import requests

API_KEY = "e41a6751534c342106fe40c9f669e733"
city = "Bhubaneswar"

url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"

response = requests.get(url)

print(response.status_code)
print(response.json())