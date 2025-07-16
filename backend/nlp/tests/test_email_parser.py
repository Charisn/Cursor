"""Unit tests for email parser module."""

import pytest
from datetime import datetime

from src.email_parser import EmailCleaner, EmailFetcher
from src.models import EmailMessage


class TestEmailCleaner:
    """Test EmailCleaner functionality."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.cleaner = EmailCleaner()
    
    def test_clean_html(self):
        """Test HTML to text conversion."""
        html = "<h1>Hello</h1><p>This is a <b>test</b> email.</p><script>alert('evil')</script>"
        result = self.cleaner.clean_html(html)
        
        assert "Hello" in result
        assert "test email" in result
        assert "<h1>" not in result
        assert "alert" not in result
    
    def test_remove_signatures(self):
        """Test signature removal."""
        text = """
        Hi there,
        
        I would like to book a room.
        
        --
        Best regards,
        John Doe
        Sent from my iPhone
        """
        
        result = self.cleaner.remove_signatures(text)
        assert "book a room" in result
        assert "Best regards" not in result
        assert "Sent from my iPhone" not in result
    
    def test_remove_quotes(self):
        """Test quoted content removal."""
        text = """
        Hi,
        
        I need availability for tomorrow.
        
        On Mon, Jan 1, 2024 at 10:00 AM John <john@example.com> wrote:
        > Original message here
        > Quote line 2
        """
        
        result = self.cleaner.remove_quotes(text)
        assert "availability for tomorrow" in result
        assert "Original message" not in result
        assert "Quote line 2" not in result
    
    def test_normalize_whitespace(self):
        """Test whitespace normalization."""
        text = "Hello    world\n\n\n\nNew paragraph"
        result = self.cleaner.normalize_whitespace(text)
        
        assert "Hello world" in result
        assert "    " not in result
        # Should have at most double line breaks
        assert "\n\n\n" not in result


class TestEmailFetcher:
    """Test EmailFetcher functionality."""
    
    def test_email_message_creation(self):
        """Test creating EmailMessage with validation."""
        email = EmailMessage(
            subject="Test Subject",
            body="Test body content",
            sender="test@example.com",
            received_at=datetime.now(),
            message_id="test-123"
        )
        
        assert email.subject == "Test Subject"
        assert email.body == "Test body content"
        assert email.sender == "test@example.com"
    
    def test_email_message_validation(self):
        """Test EmailMessage validation."""
        # Empty body should raise validation error
        with pytest.raises(ValueError):
            EmailMessage(
                subject="Test",
                body="   ",  # Only whitespace
                sender="test@example.com",
                received_at=datetime.now(),
                message_id="test-123"
            ) 