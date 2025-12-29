import subprocess
import logging
from typing import List, Dict, Any

class EmailClient:
    def fetch_emails(self, account: str, mailbox: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Fetches unread emails from the specified account and mailbox using direct AppleScript.
        """

        
        # NOTE: AppleScript JSON construction is fragile with escaping.
        # A safer way is to return a delimiter-separated list and parse in Python.
        # Let's retry with a safer parsing approach.
        
        safe_script = f"""
        tell application "Mail"
            tell account "{account}"
                tell mailbox "{mailbox}"
                    set unreadMsgs to (messages whose read status is false)
                    set msgCount to count of unreadMsgs
                    
                    if msgCount is 0 then return ""
                    
                    if msgCount > {limit} then
                        set targetMsgs to items 1 thru {limit} of unreadMsgs
                    else
                        set targetMsgs to unreadMsgs
                    end if
                    
                    set output to ""
                    repeat with msg in targetMsgs
                        set msgSubject to subject of msg
                        set msgSender to sender of msg
                        -- Content can be huge and contain delimiters. We use a unique separator.
                        set msgContent to content of msg
                        
                        set output to output & "###MSG_START###" & linefeed
                        set output to output & "SUBJECT: " & msgSubject & linefeed
                        set output to output & "SENDER: " & msgSender & linefeed
                        set output to output & "CONTENT_START" & linefeed
                        set output to output & msgContent & linefeed
                        set output to output & "CONTENT_END" & linefeed
                    end repeat
                    return output
                end tell
            end tell
        end tell
        """

        try:
            result = subprocess.run(["osascript", "-e", safe_script], capture_output=True, text=True)
            if result.returncode != 0:
                logging.error(f"AppleScript error: {result.stderr}")
                return []
            
            return self._parse_output(result.stdout)
        except Exception as e:
            logging.error(f"Error fetching emails: {e}")
            return []

    def _parse_output(self, raw_text: str) -> List[Dict[str, Any]]:
        emails = []
        current_email = {}
        lines = raw_text.splitlines()
        in_content = False
        content_buffer = []
        
        for line in lines:
            if line.strip() == "###MSG_START###":
                if current_email:
                    if in_content: # Close previous content if unclosed
                         current_email["content"] = "\n".join(content_buffer).strip()
                    emails.append(current_email)
                current_email = {}
                in_content = False
                content_buffer = []
            elif line.startswith("SUBJECT: ") and not in_content:
                current_email["subject"] = line[9:]
            elif line.startswith("SENDER: ") and not in_content:
                current_email["sender"] = line[8:]
            elif line.strip() == "CONTENT_START":
                in_content = True
            elif line.strip() == "CONTENT_END":
                in_content = False
                current_email["content"] = "\n".join(content_buffer).strip()
            elif in_content:
                content_buffer.append(line)
                
        if current_email:
            emails.append(current_email)
            
        return emails
