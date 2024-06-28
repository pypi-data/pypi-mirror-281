import requests
from dotenv import load_dotenv
# Load environment variables from .env file

load_dotenv()

api_key = '424c3305adfa842539b42ac627e7074f'
headers = {'access_token': api_key}

# Call root_length_measurement component
response = requests.get('http://127.0.0.1:8000/root_length_measurement', headers=headers)

if response.status_code == 200:
    print("Response:", response.json())
else:
    print("Error:", response.status_code, response.text)