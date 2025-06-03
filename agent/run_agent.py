import requests
import json
import re # For robust train number extraction (still useful as a fallback/validation)
import logging
import os # For environment variables, though API_KEY is hardcoded as per instructions

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Configuration ---
# The URL of the MCP server. Ensure this matches where your MCP server is running.
MCP_SERVER_URL = "http://127.0.0.1:5000"

# Gemini API Configuration
# IMPORTANT: Leave this as an empty string. The Canvas environment will provide the API key at runtime.
GEMINI_API_KEY = "USEAPIKEY"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"



def call_mcp_tool(tool_name: str, payload: dict) -> dict:
    """
    Sends a request to the MCP server to execute a specified tool.

    Args:
        tool_name (str): The name of the tool to call (e.g., "get_train_status").
        payload (dict): A dictionary containing the arguments for the tool.

    Returns:
        dict: The JSON response from the MCP server, or an error dictionary.
    """
    url = f"{MCP_SERVER_URL}/tool/{tool_name}"
    logging.info(f"Agent: Attempting to call MCP tool '{tool_name}' at {url} with payload: {payload}")
    try:
        # Send a POST request with the payload as JSON
        response = requests.post(url, json=payload)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        logging.info(f"Agent: Successfully received response from '{tool_name}'.")
        return response.json()
    except requests.exceptions.ConnectionError:
        logging.error("Agent: Could not connect to the MCP server. Is it running?")
        return {"error": "Could not connect to the MCP server. Please ensure it is running."}
    except requests.exceptions.HTTPError as e:
        logging.error(f"Agent: HTTP error occurred while calling '{tool_name}': {e.response.status_code} - {e.response.text}")
        return {"error": f"HTTP error occurred: {e.response.status_code} - {e.response.text}"}
    except json.JSONDecodeError:
        logging.error(f"Agent: Failed to decode JSON response from '{tool_name}'. Response: {response.text}")
        return {"error": "Received non-JSON response from server."}
    except Exception as e:
        logging.error(f"Agent: An unexpected error occurred while calling '{tool_name}': {e}")
        return {"error": f"An unexpected error occurred: {e}"}

def call_gemini_api(user_query: str) -> dict:
    """
    Calls the Gemini API to understand user intent and extract entities.

    Args:
        user_query (str): The user's input query.

    Returns:
        dict: Parsed JSON response from Gemini, or an error dictionary.
    """
    chat_history = []
    chat_history.append({"role": "user", "parts": [{"text": user_query}]}) 

    # Define the prompt for Gemini to guide its response
    prompt = f"""
    Analyze the following user query and determine if it's a request for Indian Railways train status.
    If it is, extract the 5-digit train number.
    If no 5-digit train number is explicitly mentioned, return null for train_number.

    Respond with a JSON object in the following format:
    {{
        "intent": "get_train_status" | "unclear",
        "train_number": "XXXXX" | null
    }}

    User query: "{user_query}"
    """

    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": {
                "type": "OBJECT",
                "properties": {
                    "intent": {
                        "type": "STRING",
                        "enum": ["get_train_status", "unclear"]
                    },
                    "train_number": {
                        "type": "STRING",
                        "nullable": True,
                        "pattern": "^\\d{5}$"
                    }
                },
                "required": ["intent"],
                "propertyOrdering": ["intent", "train_number"]
            }
        }
    }

    headers = {'Content-Type': 'application/json'}

    api_url_with_key = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}" if GEMINI_API_KEY else GEMINI_API_URL

    logging.info(f"Agent: Calling Gemini API with prompt for query: '{user_query}'")
    try:
        response = requests.post(api_url_with_key, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        result = response.json()

        if result.get("candidates") and result["candidates"][0].get("content") and \
           result["candidates"][0]["content"].get("parts") and \
           result["candidates"][0]["content"]["parts"][0].get("text"):
            json_text = result["candidates"][0]["content"]["parts"][0]["text"]
            parsed_json = json.loads(json_text)
            logging.info(f"Agent: Gemini API response: {parsed_json}")
            return parsed_json
        else:
            logging.warning(f"Agent: Unexpected Gemini API response structure: {result}")
            return {"error": "Unexpected response from Gemini API."}

    except requests.exceptions.ConnectionError:
        logging.error("Agent: Could not connect to the Gemini API. Check network connection.")
        return {"error": "Could not connect to the Gemini API."}
    except requests.exceptions.HTTPError as e:
        logging.error(f"Agent: HTTP error from Gemini API: {e.response.status_code} - {e.response.text}")
        return {"error": f"HTTP error from Gemini API: {e.response.status_code} - {e.response.text}"}
    except json.JSONDecodeError:
        logging.error(f"Agent: Failed to decode JSON from Gemini API. Response: {response.text}")
        return {"error": "Failed to decode JSON from Gemini API."}
    except Exception as e:
        logging.error(f"Agent: An unexpected error occurred during Gemini API call: {e}")
        return {"error": f"An unexpected error occurred during Gemini API call: {e}"}

def chat_with_agent():
    """
    The main conversational loop for the AI agent.
    It processes user input using Gemini for intent recognition and then
    uses MCP tools accordingly.
    """
    print("Welcome! I can help you find Indian Railways train status.")
    print("Type 'exit' to quit.")
    print("Example query: 'What is the status of train 12301?' or 'Check train 12137 status.'")

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() == 'exit':
            print("Agent: Goodbye!")
            logging.info("Agent session ended.")
            break

        # Use Gemini API for intent recognition and entity extraction
        gemini_response = call_gemini_api(user_input)

        if "error" in gemini_response:
            print(f"Agent: I'm having trouble understanding right now: {gemini_response['error']}")
            continue

        intent = gemini_response.get("intent")
        train_number = gemini_response.get("train_number")

        if intent == "get_train_status":
            if train_number:
                print(f"Agent: Looking up status for train number {train_number}...")
                # Call the 'get_train_status' tool on the MCP server
                tool_response = call_mcp_tool("get_train_status", {"train_number": train_number})

                if "error" in tool_response:
                    print(f"Agent: Sorry, I encountered an issue: {tool_response['error']}")
                else:
                    print(f"Agent: The status for train {tool_response['train_number']} ({tool_response['name']}) is: {tool_response['status']}")
            else:
                print("Agent: I understand you want train status, but I couldn't find a 5-digit train number in your query. Please provide it (e.g., '12301').")
        else:
            print("Agent: I can currently only help with Indian Railways train status queries. Please ask about a train's status.")

if __name__ == '__main__':
    logging.info("Starting AI Agent...")
    chat_with_agent()
