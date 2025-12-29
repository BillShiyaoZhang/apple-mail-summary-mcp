from fastmcp import FastMCP
from .processor import PaperProcessor
from .email_client import EmailClient
import logging
import json
import os

# Initialize Logger
logging.basicConfig(level=logging.INFO)

# Create MCP Server
mcp = FastMCP("apple-mail-mcp")

# Initialize Helpers
processor = PaperProcessor()
email_client = EmailClient()

@mcp.tool()
def fetch_emails(account: str | None = None, mailbox: str | None = None, limit: int = 5) -> str:
    """
    Fetches the latest unread emails from a specified account and mailbox.
    
    Args:
        account: The name of the account in Apple Mail (e.g., "iCloud", "Gmail"). 
                 Defaults to APPLE_MAIL_SUMMARY_MCP_ACCOUNT env var if not set.
        mailbox: The name of the mailbox (e.g., "Inbox", "Google Scholar"). 
                 Defaults to "Inbox" or APPLE_MAIL_SUMMARY_MCP_MAILBOX env var.
        limit: Max number of emails to fetch. Defaults to 5.
        
    Returns:
        A JSON list of emails with subject, sender, and content.
    """
    # Resolve defaults from environment variables
    target_account = account or os.environ.get("APPLE_MAIL_SUMMARY_MCP_ACCOUNT")
    target_mailbox = mailbox or os.environ.get("APPLE_MAIL_SUMMARY_MCP_MAILBOX") or "Inbox"
    
    if not target_account:
        return "Error: No account specified. Please provide the 'account' argument or set the APPLE_MAIL_SUMMARY_MCP_ACCOUNT environment variable."

    try:
        emails = email_client.fetch_emails(target_account, target_mailbox, limit)
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
