# Apple Mail MCP Server

A Model Context Protocol (MCP) server for macOS that allows AI agents to interact with the local **Apple Mail** application. This server enables LLMs to fetch emails from specific accounts and mailboxes, and includes specialized tools for parsing academic paper alerts.

## Features

- 📧 **Fetch Emails**: Retrieve the latest unread emails from any configured Apple Mail account and mailbox.
- 🎓 **Scholar Tools**: specialized parsing for Google Scholar Alert emails to extract paper titles and links.
- 🔒 **Local & Secure**: Runs locally on your machine, communicating directly with Apple Mail via AppleScript.

## Prerequisites

- **macOS**: This server relies on `osascript` (AppleScript) to communicate with Apple Mail. It **will not work** on Windows or Linux.
- **Apple Mail**: Must be set up and running with your email accounts configured.
- **Python 3.10+**
- **uv** (recommended for package management) or standard pip.

## Installation

### Using uv (Recommended)

```bash
git clone https://github.com/yourusername/apple-mail-mcp.git
cd apple-mail-mcp
uv pip install -e .
```

### Using pip

```bash
git clone https://github.com/yourusername/apple-mail-mcp.git
cd apple-mail-mcp
pip install -e .
```

## Usage

### 1. Identify your Mail Configuration

To use this server, you need to know the exact names of your **Accounts** and **Mailboxes** as they appear in Apple Mail.

You can find these by hovering over the mailbox in the Mail app sidebar, or by running this simple AppleScript in 'Script Editor.app':

```applescript
tell application "Mail"
    get name of every account
end tell
```

### 2. Configuration for Claude Desktop

You can add this server to your `claude_desktop_config.json` in two ways:

#### Option A: Running directly from GitHub via `uvx` (No manual install needed)
This is the easiest way to try it out without manually cloning the generic repo.

```json
{
  "mcpServers": {
    "apple-mail": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/yourusername/apple-mail-mcp.git", 
        "apple-mail-mcp" 
      ]
    }
  }
}
```

#### Option B: Running from a Local Clone (Development)

If you have cloned the repository locally and want to make changes:

```json
{
  "mcpServers": {
    "apple-mail": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/apple-mail-mcp",
        "run",
        "apple-mail-mcp"
      ]
    }
  }
}
```

> **Note**: For Option B to work, make sure `uv` is in your system PATH.

### 3. Running the Server Manually
You can also run the server directly if needed:
```bash
python -m apple_mail_mcp.server
```

### 4. Available Tools

#### `fetch_emails(account: str, mailbox: str = "Inbox", limit: int = 5)`
Fetches a list of unread emails from a specific source.
- **account**: The exact name of the account (e.g., "iCloud", "Exchange", "Personal").
- **mailbox**: The mailbox name (e.g., "Inbox", "Spam", "Google Scholar").
- **limit**: Maximum number of emails to retrieve.

#### `extract_scholar_links(html_content: str)`
A utility tool to parse the HTML content of a Google Scholar Alert email and return structured data (Title, URL).
- **html_content**: The raw HTML body of the email.

## Development

Project structure:
- `src/apple_mail_mcp/email_client.py`: Handles AppleScript communication.
- `src/apple_mail_mcp/processor.py`: Contains HTML parsing logic (BeautifulSoup).
- `src/apple_mail_mcp/server.py`: Defines the FastMCP server and tools.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT](LICENSE)
