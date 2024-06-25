# Main API
import requests

def test_print():
    print('This is Ampari 0.1!')


# The call_context API will be designed to call outside context for the user using the Ampari API and their access token
def call_context(user_prompt: str, access_token: str):
    pass

    # Basically just make a call to the api using the user 


import requests

def serve(api_token, user_prompt):
    url = 'https://www.ampari-api.com/python-lib/serve'
    headers = {'Content-Type': 'application/json'}
    data = {
        'api_token': api_token,
        'prompt': user_prompt
    }
    
    print("Request Headers:", headers)
    print("Request Data:", data)
    
    response = requests.post(url, json=data, headers=headers)
    
    # Rest of your function remains the same

    
    if response.status_code == 200:
        try:
            # Attempt to parse the JSON response
            json_response = response.json()
            print("Serve Response:", json_response)
        except ValueError as e:
            print(response)
            print("Error parsing JSON:", e)
            print("Response Content:", response.text)  # Print the raw response content for debugging
    else:
        print("Error:", response.status_code, response.text)

# Function to call the '/reg_api' endpoint
def register(api_token, endpoint, documentation, description, api_key):
    url = 'https://www.ampari-api.com/python-lib/'  # Replace with your server's URL
    headers = {'Content-Type': 'application/json'}
    data = {
        'api_token': api_token,
        'endpoint': endpoint,
        'documentation': documentation,
        'description': description,
        'api_key': api_key
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        return "API successfully registered"
    else:
        return {"error": f"Error {response.status_code}: {response.text}"}

