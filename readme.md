Indian Railways Train Status AI Agent with MCP

This project demonstrates a basic Multi-Agent Communication Protocol (MCP) setup for an AI agent that can provide Indian Railways train status.

The system consists of two main components:

An MCP Server that hosts a get_train_status tool.

An AI Agent that interacts with the user and utilizes both the local MCP server and the Gemini API for natural language understanding.

📁 Project Structure

mcp_server.py: A Flask-based MCP server that exposes a get_train_status tool.

ai_agent.py: The AI agent that handles user interaction, uses the Gemini API for intent recognition and entity extraction, and calls the get_train_status tool.

requirements.txt: Lists the Python dependencies required for the project.

✨ Features

Modular Design: Clean separation between the AI agent and the tool-providing MCP server.

Natural Language Understanding: Powered by the Gemini API to interpret user queries and extract train numbers.

Tool-Based Execution: The AI agent uses tools via MCP to execute tasks.

Simulated Data: Uses a hardcoded dictionary to simulate train status data.

⚙️ Setup and Installation

1. Clone the Repository

Ensure you have mcp_server.py, ai_agent.py, and requirements.txt in the same directory.

2. Create a Virtual Environment (Recommended)

python -m venv train_mcp_env
source train_mcp_env/bin/activate  # On Windows: train_mcp_env\Scripts\activate

3. Install Dependencies

pip install -r requirements.txt

🚀 How to Run

You will need two terminal windows: one for the MCP server and one for the AI agent.

1. Run the MCP Server

python mcp_server.py

You should see output indicating the Flask server is running, usually at http://127.0.0.1:5000.

2. Run the AI Agent

In a new terminal window, execute:

python ai_agent.py

You’ll see a welcome message:

Welcome! I can help you find Indian Railways train status.Type 'exit' to quit.Example query: 'What is the status of train 12301?' or 'Check train 12137 status.'

💬 Interacting with the AI Agent

Type your queries like:

What is the status of train 12301?

Check train 12137 status.

Tell me about train 12834.

Is train 12951 on time?

Get information for train number 11013.

What about train 99999? (Triggers a "not found" response)

Hello, how are you? (The agent will indicate it only handles train status)

To exit the agent, type:

exit

⚠️ Important Notes

Simulated Data: The mcp_server.py uses a hardcoded TRAIN_STATUS_DB. Replace it with actual API calls for real-world deployment.

Gemini API Key:

GEMINI_API_KEY in ai_agent.py is currently empty.

If using in Google Cloud Canvas, it's automatically provided.

If running locally, set it manually with your Gemini API key.

Error Handling: Includes basic handling for network failures, invalid input, and tool errors.

Port Usage: MCP server runs on port 5000 by default. Ensure this port is available.

📄 License

This project is for educational and demo purposes only. Replace simulated components for production use.

