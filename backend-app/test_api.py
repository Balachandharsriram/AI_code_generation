import requests
import json

# ====================================================================
# CONFIGURATION
# ====================================================================

# The text we want to convert to PLC code.
description = "When the start button is pressed, turn on motor 1 for 10 seconds. Include a stop button."

# Set this variable to either "st" for Structured Text or "ld" for Ladder Diagram.
output_format = "ld"

# We build the URL based on your choice.
url = f"http://127.0.0.1:8000/generate_{output_format}"

# We're sending our description in a JSON format.
data = {"description": description}

# ====================================================================
# API TEST LOGIC
# ====================================================================
try:
    # We make a POST request to our server.
    response = requests.post(url, json=data)
    response.raise_for_status() # This will raise an exception for bad status codes (4xx or 5xx)

    # If the response is successful, we print the content.
    if response.headers.get('content-type') == 'application/json':
        response_data = response.json()
        print("API Call Successful! Here is the ld response:")
        print(json.dumps(response_data, indent=2))
        
        # We can also check for validation results if we are testing ST
        if output_format == "ld" and "validation" in response_data:
            print("\n--- Validation Results ---")
            if response_data["validation"]["is_valid"]:
                print("Code is syntactically valid!")
            else:
                print("Code has validation errors!")
                if response_data["validation"]["errors"]:
                    print("\nErrors:")
                    for error in response_data["validation"]["errors"]:
                        print(f"- {error}")
                if response_data["validation"]["warnings"]:
                    print("\nWarnings:")
                    for warning in response_data["validation"]["warnings"]:
                        print(f"- {warning}")
    else:
        print("Received non-JSON response:")
        print(response.text)

except requests.exceptions.RequestException as e:
    # This catches any errors during the request (e.g., server not running).
    print(f"An error occurred: {e}")