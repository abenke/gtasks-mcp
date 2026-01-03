# Google Tasks MCP Server

A Model Context Protocol (MCP) server that provides access to your Google Tasks. This server enables LLMs (like Claude) to list, create, update, complete, and delete your Google Tasks.

## Features

- **List Task Lists**: View all your task lists.
- **Manage Tasks**: Create, update, delete, and complete tasks.
- **Task Details**: Set due dates, notes, and move tasks (subtasks).
- **FastMCP**: Built using the `fastmcp` library for easy integration.

## Setup

### Prerequisites

- Python 3.10 or higher
- A Google Cloud Platform (GCP) Project
- `uv` (recommended) or `pip`

### Installation

1.  Clone this repository:
    ```bash
    git clone https://github.com/yourusername/gtasks-mcp.git
    cd gtasks-mcp
    ```

2.  Create a virtual environment and install dependencies:
    ```bash
    # Using uv (faster)
    uv venv
    source .venv/bin/activate
    uv pip install -r requirements.txt

    # OR using pip
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

### Google Cloud Setup

To use this server, you need to set up a Google Cloud project and enable the Tasks API.

1.  **Create a Project**: Go to the [Google Cloud Console](https://console.cloud.google.com/) and create a new project.
2.  **Enable API**:
    *   Go to **APIs & Services** > **Library**.
    *   Search for "Google Tasks API" and click **Enable**.
3.  **Configure Consent Screen**:
    *   Go to **APIs & Services** > **OAuth consent screen**.
    *   Select **External** (unless you are a Google Workspace user and want Internal).
    *   Fill in the required App Information (App name: "GTasks MCP", User support email, Developer contact email).
    *   Click **Save and Continue**.
    *   **Scopes**: Click **Add or Remove Scopes**. Filter for `tasks`. Select `https://www.googleapis.com/auth/tasks` (Access to your tasks).
    *   Click **Update** and then **Save and Continue**.
    *   **Test Users**: Add your own email address as a test user. This is critical while the app is in "Testing" mode.
4.  **Create Credentials**:
    *   Go to **APIs & Services** > **Credentials**.
    *   Click **Create Credentials** > **OAuth client ID**.
    *   Application type: **Desktop app**.
    *   Name: "GTasks MCP User".
    *   Click **Create**.
5.  **Download Client Secret**:
    *   Download the JSON file for your new OAuth client.
    *   **Rename** the file to `client_secret.json`.
    *   **Move** it to the root directory of this project.

### Usage with Claude for Desktop

Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "google-tasks": {
      "command": "/absolute/path/to/your/venv/bin/python",
      "args": [
        "/absolute/path/to/gtasks-mcp/server.py"
      ]
    }
  }
}
```

*Note: Replace `/absolute/path/to/` with the actual full paths on your machine.*

## Authentication

When you first run the server (or when Claude tries to use it), it will open a browser window asking you to log in with your Google account.
1.  Select the account you added as a Test User.
2.  You will likely see a "Google hasn't verified this app" warning. This is expected for personal testing apps.
3.  Click **Advanced** > **Go to GTasks MCP (unsafe)**.
4.  Click **Continue** to grant access.
5.  The browser will show "The authentication flow has completed". You can close it.

A `token.json` file will be created to store your credentials for future use.

## License

MIT
