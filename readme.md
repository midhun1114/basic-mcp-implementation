Indian Railways Train Status AI Agent with MCP
This project demonstrates a basic Multi-Agent Communication Protocol (MCP) setup for an AI agent that can provide Indian Railways train status. The system consists of two main components: an MCP Server that hosts a "tool" for fetching train status, and an AI Agent that interacts with the user and utilizes both the local MCP server and the Gemini API for natural language understanding.

Project Structure
mcp_server.py: The Flask-based MCP server that exposes a get_train_status tool.

ai_agent.py: The AI agent that handles user interaction, uses the Gemini API for intent recognition and entity extraction, and calls the get_train_status tool on the MCP server.

requirements.txt: Lists the Python dependencies required for the project.

Features
Modular Design: Separation of concerns between the AI agent and the tool-providing MCP server.

Natural Language Understanding: Uses the Gemini API to understand user queries and extract train numbers.

Tool-Based Execution: The AI agent calls a specific tool on the MCP server to retrieve train status.

Simulated Data: The MCP server uses a hardcoded dictionary to simulate train status data.

Setup and Installation
Clone the Repository (or save the files):
Ensure you have mcp_server.py, ai_agent.py, and requirements.txt in the same directory.

Create a Virtual Environment (Recommended):

python -m venv train_mcp_env
source train_mcp_env/bin/activate  # On Windows: train_mcp_env\Scripts\activate

Install Dependencies:
Navigate to the project directory in your terminal and install the required Python packages:

pip install -r requirements.txt

How to Run
To operate the system, you need to run the MCP Server and the AI Agent in separate terminal windows.

1. Run the MCP Server
Open your first terminal window and execute:

python mcp_server.py

You should see output indicating that the Flask server is running, typically on http://127.0.0.1:5000. Keep this terminal window open and running.

2. Run the AI Agent
Open a second terminal window, navigate to the same project directory, and execute:

python ai_agent.py

The AI agent will start, and you will see a welcome message:

Welcome! I can help you find Indian Railways train status.
Type 'exit' to quit.
Example query: 'What is the status of train 12301?' or 'Check train 12137 status.'

Interacting with the AI Agent
Now, in the second terminal where the AI agent is running, you can type your queries.

Examples:

What is the status of train 12301?

Check train 12137 status.

Tell me about train 12834.

Is train 12951 on time?

Get information for train number 11013.

What about train 99999? (This will trigger a "not found" message as it's not in the simulated database)

Hello, how are you? (The agent will indicate it can only help with train status)

To exit the agent, type exit.

Important Notes
Simulated Data: The mcp_server.py uses a hardcoded TRAIN_STATUS_DB for demonstration purposes. In a real-world application, this would be replaced with actual API calls to a reliable Indian Railways data provider (which may require API keys and proper authentication).

Gemini API Key: The GEMINI_API_KEY in ai_agent.py is left as an empty string. If running in an environment like Google Cloud Canvas, the API key is automatically provided at runtime. If running locally outside such an environment, you would need to manually set this variable with your actual Gemini API key.

Error Handling: Both the agent and the server include basic error handling for network issues, invalid requests, and unexpected responses.

Port: The MCP server runs on port 5000 by default. Ensure this port is not blocked or in use by another application.