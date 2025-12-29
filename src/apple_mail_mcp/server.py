from fastmcp import FastMCP
from .processor import PaperProcessor
from .email_client import EmailClient
import logging
import json

# Initialize Logger
logging.basicConfig(level=logging.INFO)

# Create MCP Server
mcp = FastMCP("paper-processor")

# Initialize Helpers
processor = PaperProcessor()
email_client = EmailClient()

@mcp.tool()
def fetch_scholar_emails(count: int = 5) -> str:
    """
    Fetches the latest unread emails from 'Google Scholar' mailbox.
    Returns a JSON list of emails with subject, sender, and content.
    """
    try:
        # Note: Account name "XJTLU" is hardcoded from original extraction.
        # Ideally this should be configurable, but keeping as is for migration parity.
        emails = email_client.fetch_emails("XJTLU", "Google Scholar", count)
        return json.dumps(emails, indent=2)
    except Exception as e:
        return f"Error fetching emails: {str(e)}"

@mcp.tool()
def process_scholar_html(html_content: str) -> str:
    """
    Extracts paper links from Google Scholar Alert HTML content.
    Returns a JSON string of a list of papers with 'title' and 'url'.
    """
    try:
        links = processor.extract_links(html_content)
        return json.dumps(links, indent=2)
    except Exception as e:
        return f"Error extracting links: {str(e)}"

if __name__ == "__main__":
    mcp.run()
