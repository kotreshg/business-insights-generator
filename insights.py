import requests
import pandas as pd

# IBM API Configurations
API_KEY = "m81X_WQ5U9fPcg01l6MUoQhnGuRa9QJ0z-iOPGwIOUE4"
PROJECT_ID = "b2b3a5ab-bd3f-4a7d-a11f-c223672b9033"
IAM_URL = "https://iam.cloud.ibm.com/identity/token"
AI_URL = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"


def get_ibm_access_token():
    """Fetches the IBM Cloud authentication token using the API key."""
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = f"grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={API_KEY}"

    response = requests.post(IAM_URL, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception(f"Failed to get IBM Access Token: {response.text}")


def generate_insights(df):
    """Takes a pandas DataFrame, extracts relevant data, and calls AI model to generate insights."""
    # Convert DataFrame to text format (limit characters to avoid excessive API load)
    data_text = df.head(10).to_string()

    # AI Prompt
    input_text = f"""
    Analyze the following business data and generate key insights:Consider trends, correlations, and the impact of marketing spend,any advices. Provide a detailed breakdown.
    {data_text}

    
    """

    # Fetch a fresh access token
    access_token = get_ibm_access_token()

    body = {
        "input": input_text,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 500,
            "repetition_penalty": 1.05
        },
        "model_id": "ibm/granite-13b-instruct-v2",
        "project_id": PROJECT_ID
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"  # Use dynamic token
    }

    # Call IBM AI API
    response = requests.post(AI_URL, headers=headers, json=body)

    if response.status_code == 200:
        data = response.json()
        generated_text = data.get("results",
                                  [{}])[0].get("generated_text",
                                               "No insights available")
        return generated_text  # Return only the AI-generated text
    else:
        return f"Error: {response.text}"
