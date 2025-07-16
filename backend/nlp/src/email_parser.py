"""Email parsing and preprocessing module."""

import email
import re
from datetime import datetime
from email.message import EmailMessage as StdEmailMessage
from typing import List, Optional

import html2text
from bs4 import BeautifulSoup
from imapclient import IMAPClient
from email_validator import validate_email, EmailNotValidError

from .config import get_settings
from .models import EmailMessage


class EmailCleaner:
    """Cleans and preprocesses email content."""
    
    def __init__(self):
        """Initialize email cleaner."""
        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = True
        self.html_converter.ignore_images = True
        self.html_converter.body_width = 0  # No line wrapping
        
        # Common signature patterns
        self.signature_patterns = [
            r'--\s*\n.*',  # Standard signature delimiter
            r'Best regards,.*',
            r'Sincerely,.*',
            r'Thanks,.*',
            r'Sent from my.*',
            r'This email was sent.*',
            r'________________________________.*',  # Outlook separator
        ]
        
        # Quote patterns (replied/forwarded emails)
        self.quote_patterns = [
            r'On .* wrote:.*',
            r'From:.*\nSent:.*\nTo:.*\nSubject:.*',
            r'>.*',  # Quoted lines
            r'-----Original Message-----.*',
        ]
    
    def clean_html(self, html_content: str) -> str:
        """Convert HTML to clean text."""
        # Use BeautifulSoup for initial cleaning
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Convert to text using html2text
        text = self.html_converter.handle(str(soup))
        
        return text.strip()
    
    def remove_signatures(self, text: str) -> str:
        """Remove email signatures."""
        for pattern in self.signature_patterns:
            text = re.sub(pattern, '', text, flags=re.DOTALL | re.IGNORECASE)
        
        return text.strip()
    
    def remove_quotes(self, text: str) -> str:
        """Remove quoted/forwarded content."""
        for pattern in self.quote_patterns:
            text = re.sub(pattern, '', text, flags=re.DOTALL | re.IGNORECASE)
        
        return text.strip()
    
    def normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace and line breaks."""
        # Replace multiple spaces with single space
        text = re.sub(r' +', ' ', text)
        
        # Replace multiple line breaks with double line break
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text.strip()
    
    def clean_email_body(self, raw_body: str, is_html: bool = False) -> str:
        """Clean email body text."""
        if is_html:
            text = self.clean_html(raw_body)
        else:
            text = raw_body
        
        # Remove quotes and signatures
        text = self.remove_quotes(text)
        text = self.remove_signatures(text)
        
        # Normalize whitespace
        text = self.normalize_whitespace(text)
        
        return text


class EmailFetcher:
    """Fetches emails from IMAP server."""
    
    def __init__(self):
        """Initialize email fetcher."""
        self.settings = get_settings()
        self.cleaner = EmailCleaner()
    
    def connect(self) -> IMAPClient:
        """Connect to IMAP server."""
        client = IMAPClient(
            host=self.settings.imap_server,
            port=self.settings.imap_port,
            use_uid=True,
            ssl=self.settings.imap_use_tls
        )
        
        client.login(
            self.settings.imap_username,
            self.settings.imap_password
        )
        
        return client
    
    def parse_email_message(self, raw_message: bytes) -> Optional[EmailMessage]:
        """Parse raw email message into structured format."""
        try:
            # Parse the email
            msg = email.message_from_bytes(raw_message)
            
            # Extract basic fields
            subject = msg.get('Subject', '').strip()
            sender = msg.get('From', '').strip()
            message_id = msg.get('Message-ID', '').strip()
            date_str = msg.get('Date', '')
            
            # Validate sender email
            try:
                validated_email = validate_email(sender)
                sender = validated_email.email
            except EmailNotValidError:
                # Skip invalid sender emails
                return None
            
            # Parse date
            try:
                received_at = email.utils.parsedate_to_datetime(date_str)
            except (TypeError, ValueError):
                received_at = datetime.now()
            
            # Extract body
            body = self._extract_body(msg)
            if not body:
                return None
            
            return EmailMessage(
                subject=subject,
                body=body,
                sender=sender,
                received_at=received_at,
                message_id=message_id
            )
            
        except Exception as e:
            # Log error and skip malformed emails
            print(f"Error parsing email: {e}")
            return None
    
    def _extract_body(self, msg: StdEmailMessage) -> str:
        """Extract and clean email body."""
        body = ""
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get('Content-Disposition', ''))
                
                # Skip attachments
                if 'attachment' in content_disposition:
                    continue
                
                if content_type == 'text/plain':
                    charset = part.get_content_charset() or 'utf-8'
                    payload = part.get_payload(decode=True)
                    if payload:
                        try:
                            text = payload.decode(charset, errors='ignore')
                            body = self.cleaner.clean_email_body(text, is_html=False)
                            break  # Prefer plain text
                        except (UnicodeDecodeError, LookupError):
                            continue
                
                elif content_type == 'text/html' and not body:
                    charset = part.get_content_charset() or 'utf-8'
                    payload = part.get_payload(decode=True)
                    if payload:
                        try:
                            html = payload.decode(charset, errors='ignore')
                            body = self.cleaner.clean_email_body(html, is_html=True)
                        except (UnicodeDecodeError, LookupError):
                            continue
        else:
            # Single part message
            content_type = msg.get_content_type()
            charset = msg.get_content_charset() or 'utf-8'
            payload = msg.get_payload(decode=True)
            
            if payload:
                try:
                    if content_type == 'text/html':
                        html = payload.decode(charset, errors='ignore')
                        body = self.cleaner.clean_email_body(html, is_html=True)
                    else:
                        text = payload.decode(charset, errors='ignore')
                        body = self.cleaner.clean_email_body(text, is_html=False)
                except (UnicodeDecodeError, LookupError):
                    pass
        
        return body
    
    def fetch_unread_emails(self, folder: str = 'INBOX') -> List[EmailMessage]:
        """Fetch unread emails from specified folder."""
        emails = []
        
        try:
            with self.connect() as client:
                client.select_folder(folder)
                
                # Search for unread emails
                message_ids = client.search(['UNSEEN'])
                
                for msg_id in message_ids:
                    # Fetch the email
                    response = client.fetch([msg_id], ['RFC822'])
                    raw_message = response[msg_id][b'RFC822']
                    
                    # Parse the email
                    parsed_email = self.parse_email_message(raw_message)
                    if parsed_email:
                        emails.append(parsed_email)
                    
                    # Mark as read
                    client.add_flags([msg_id], ['\\Seen'])
                
        except Exception as e:
            print(f"Error fetching emails: {e}")
        
        return emails
    
    def fetch_recent_emails(self, folder: str = 'INBOX', limit: int = 10) -> List[EmailMessage]:
        """Fetch recent emails from specified folder."""
        emails = []
        
        try:
            with self.connect() as client:
                client.select_folder(folder)
                
                # Search for all emails, get most recent
                message_ids = client.search(['ALL'])
                
                # Sort by arrival time (newest first)
                message_ids = sorted(message_ids, reverse=True)[:limit]
                
                for msg_id in message_ids:
                    # Fetch the email
                    response = client.fetch([msg_id], ['RFC822'])
                    raw_message = response[msg_id][b'RFC822']
                    
                    # Parse the email
                    parsed_email = self.parse_email_message(raw_message)
                    if parsed_email:
                        emails.append(parsed_email)
                
        except Exception as e:
            print(f"Error fetching emails: {e}")
        
        return emails 