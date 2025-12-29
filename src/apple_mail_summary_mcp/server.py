from fastmcp import FastMCP
from .processor import PaperProcessor
from .email_client import EmailClient
import logging
import json

# Initialize Logger
logging.basicConfig(level=logging.INFO)

# Create MCP Server
mcp = FastMCP("apple-mail-mcp")

# Initialize Helpers
processor = PaperProcessor()
email_client = EmailClient()

@mcp.tool()
def fetch_emails(account: str, mailbox: str = "Inbox", limit: int = 5) -> str:
    """
    Fetches the latest unread emails from a specified account and mailbox.
    
    Args:
        account: The name of the account in Apple Mail (e.g., "iCloud", "Gmail").
        mailbox: The name of the mailbox (e.g., "Inbox", "Google Scholar"). Defaults to "Inbox".
        limit: Max number of emails to fetch. Defaults to 5.
        
    Returns:
        A JSON list of emails with subject, sender, and content.
    """
    try:
        emails = email_client.fetch_emails(account, mailbox, limit)
        return json.dumps(emails, indent=2)
    except Exception as e:
        return f"Error fetching emails: {str(e)}"

@mcp.tool()
def extract_scholar_links(html_content: str) -> str:
    """
    Extracts academic paper titles and URLs from HTML content (e.g. Google Scholar Alerts).
    Returns a JSON list of papers with 'title' and 'url'.
    """
    try:
        links = processor.extract_links(html_content)
        return json.dumps(links, indent=2)
    except Exception as e:
        return f"Error extracting links: {str(e)}"

def main():
    mcp.run()

if __name__ == "__main__":
    main()
