# Apple Mail MCP Server

A specialized MCP (Model Context Protocol) server designed to interact with the local **Apple Mail** application on macOS.

Currently, it features specific tools for processing Google Scholar alert emails, but the architecture allows for broader Apple Mail interaction.

## Prerequisites

- **macOS**: This server relies on `osascript` (AppleScript) to communicate with Apple Mail. It **will not work** on Windows or Linux.
- **Apple Mail**: Must be set up with the relevant accounts.
- **Python 3.10+**

## Installation

### Using uv (Recommended)

```bash
# strictly relies on fastmcp and beautifulsoup4
uv pip install -e .
```

## Usage

### Running the Server

```bash
# Run directly
python -m apple_mail_mcp.server
```

### Tools

- **`fetch_scholar_emails(count: int)`**: Fetches the latest unread emails from the "Google Scholar" mailbox (Account "XJTLU").
- **`process_scholar_html(html_content: str)`**: Extracts paper titles and URLs from Google Scholar Alert HTML content.

## Configuration

The current version has hardcoded account/mailbox names ("XJTLU" / "Google Scholar") in `server.py`. You may need to modify these values in `src/apple_mail_mcp/server.py` to match your local Apple Mail configuration.

## Development

Project structure:
- `src/apple_mail_mcp/email_client.py`: AppleScript interaction logic.
- `src/apple_mail_mcp/processor.py`: HTML parsing logic.
- `src/apple_mail_mcp/server.py`: FastMCP server definition.
