import requests

def get_api_key():
    return input("Enter your API key: ")

def validate_api_key(api_key):
    url = "https://demo-cr.twinhome.online/chatbot/api/validate-key/"  # Change to your actual domain
    response = requests.post(url, json={"api_key": api_key})
    print("Status Code:", response.status_code)
    print("Response Body:", response.text)  # Print raw response text
    try:
        return response.status_code, response.json()
    except Exception as e:
        return response.status_code, {"error": str(e)}

def save_api_key(api_key):
    with open("api_key.txt", "w") as file:
        file.write(api_key)

def main():
    api_key = get_api_key()
    status_code, response = validate_api_key(api_key)

    if status_code == 200:
        print("API key is valid and active.")
        save_api_key(api_key)
    else:
        print(response.get("error"))

if __name__ == "__main__":
    main()
