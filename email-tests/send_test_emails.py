#!/usr/bin/env python3
"""
Email testing script for Staydesk NLP system.
Sends various customer email scenarios through MailHog for testing.
"""

import smtplib
import time
from datetime import date, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(smtp_host, smtp_port, sender, recipient, subject, body):
    """Send an email through MailHog."""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = recipient
        msg['Subject'] = subject
        
        # Add body
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server = smtplib.SMTP(smtp_host, smtp_port)
        text = msg.as_string()
        server.sendmail(sender, recipient, text)
        server.quit()
        
        print(f"✅ Sent: {subject}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send '{subject}': {e}")
        return False


def main():
    """Send test email scenarios."""
    
    # MailHog configuration
    SMTP_HOST = "localhost"  # Change to "mailhog" if running in container
    SMTP_PORT = 1025
    HOTEL_EMAIL = "reservations@staydesk.com"
    
    print("🏨 Staydesk Email Testing Suite")
    print("=" * 50)
    
    # Calculate future dates for testing
    tomorrow = date.today() + timedelta(days=1)
    next_week = date.today() + timedelta(days=7)
    next_month = date.today() + timedelta(days=30)
    
    # Test scenarios
    test_emails = [
        # 1. Perfect availability request
        {
            "sender": "john.doe@example.com",
            "subject": "Room Availability Inquiry",
            "body": f"""Hi there,

I'm planning a vacation and would like to check availability for your hotel.

Details:
- Check-in date: {next_month.strftime('%B %d, %Y')}
- Number of rooms: 1
- Budget: Around $150 per night
- Preference: Ocean view if possible

Please let me know what you have available.

Thank you!
John Doe"""
        },
        
        # 2. Multi-room family request
        {
            "sender": "smith.family@gmail.com",
            "subject": "Family Vacation - 3 Rooms Needed",
            "body": f"""Dear Staydesk Resort,

We are planning a family reunion and need accommodation for our group.

Requirements:
- Check-in: {next_week.strftime('%m/%d/%Y')}
- Rooms needed: 3 rooms
- Budget: Up to $120 per room per night
- Special request: Rooms close to each other if possible

We are excited to stay at your beautiful resort!

Best regards,
The Smith Family"""
        },
        
        # 3. Last-minute booking
        {
            "sender": "urgent@business.com",
            "subject": "URGENT: Last-minute booking needed",
            "body": f"""Hello,

I need a room for tomorrow night ({tomorrow.strftime('%Y-%m-%d')}) due to a flight cancellation.

- 1 room needed
- Business traveler
- Budget flexible, up to $200/night
- City view preferred

Please confirm availability ASAP.

Thanks,
Mike Johnson"""
        },
        
        # 4. Luxury/Penthouse request
        {
            "sender": "luxury.guest@wealth.com",
            "subject": "Penthouse Suite Inquiry",
            "body": f"""Good afternoon,

I'm interested in booking your finest accommodation for a special anniversary celebration.

Details:
- Date: {(next_month + timedelta(days=5)).strftime('%B %d, %Y')}
- Duration: 3 nights  
- Guests: 2 adults
- Budget: Up to $500 per night
- Requirements: Ocean view, luxury amenities, privacy

Please send me information about your premium suites.

Sincerely,
Victoria Sterling"""
        },
        
        # 5. Budget-conscious request
        {
            "sender": "student.travel@university.edu",
            "subject": "Budget accommodation needed",
            "body": f"""Hi,

I'm a student looking for affordable accommodation for my graduation trip.

When: {(next_month + timedelta(days=10)).strftime('%m/%d/%Y')}
Rooms: 1 room
Budget: Maximum $80 per night (tight budget!)
View: Any view is fine, just need a clean room

Do you have anything available in my price range?

Thanks,
Emma Wilson"""
        },
        
        # 6. Vague request (needs clarification)
        {
            "sender": "unclear.request@email.com",
            "subject": "Room availability?",
            "body": """Hi,

Do you have rooms available soon? I'm flexible with dates.

Let me know,
Alex"""
        },
        
        # 7. Complex special requests
        {
            "sender": "special.needs@access.com",
            "subject": "Accessible Room Request",
            "body": f"""Dear Reservations Team,

I need to book an accessible room for my upcoming stay.

Check-in: {next_week.strftime('%B %d, %Y')}
Rooms: 1 room
Budget: Around $130 per night
Special requirements:
- Wheelchair accessible
- Roll-in shower
- Lower bed height
- Service dog accommodation

Please confirm you can accommodate these needs.

Best regards,
Robert Martinez"""
        },
        
        # 8. Group/Corporate booking
        {
            "sender": "events@corporation.com",
            "subject": "Corporate Event - Block Booking",
            "body": f"""Hello,

We're organizing a corporate retreat and need multiple rooms.

Event dates: {(next_month + timedelta(days=15)).strftime('%B %d, %Y')} to {(next_month + timedelta(days=17)).strftime('%B %d, %Y')}
Rooms needed: 8-10 rooms
Budget: $140-160 per room per night
Group: 20 business professionals

Do you offer group rates? Can you accommodate this size group?

Thank you,
Sarah Chen
Corporate Events Manager"""
        },
        
        # 9. Generic inquiry (not availability)
        {
            "sender": "info.seeker@curious.com",
            "subject": "Hotel amenities question",
            "body": """Hello,

I'm considering your hotel for a future stay and have some questions:

- Do you have a spa?
- What time is checkout?
- Is parking included?
- Do you allow pets?
- What restaurants are nearby?

Thanks for the information!

Best,
Patricia Williams"""
        },
        
        # 10. Spam email (should be ignored)
        {
            "sender": "spam@scammer.fake",
            "subject": "URGENT!!! You've won $1,000,000!!!",
            "body": """CONGRATULATIONS!!! 

You have been selected as our GRAND PRIZE WINNER!

Click here NOW to claim your $1,000,000 prize!!!

www.totallylegitwebsite.fake

LIMITED TIME OFFER - ACT NOW!!!"""
        }
    ]
    
    print(f"📧 Sending {len(test_emails)} test emails...")
    print()
    
    sent_count = 0
    for i, email_data in enumerate(test_emails, 1):
        print(f"📤 {i}/{len(test_emails)}: {email_data['subject'][:50]}...")
        
        success = send_email(
            SMTP_HOST, SMTP_PORT,
            email_data['sender'],
            HOTEL_EMAIL,
            email_data['subject'],
            email_data['body']
        )
        
        if success:
            sent_count += 1
        
        # Small delay between emails
        time.sleep(1)
    
    print()
    print(f"📊 Email sending complete: {sent_count}/{len(test_emails)} sent successfully")
    print(f"🌐 View emails in MailHog: http://localhost:8025")
    print()
    print("Test scenarios sent:")
    print("1. ✅ Perfect availability request (John Doe)")
    print("2. ✅ Multi-room family request (Smith Family)")  
    print("3. ✅ Last-minute booking (Mike Johnson)")
    print("4. ✅ Luxury penthouse request (Victoria Sterling)")
    print("5. ✅ Budget-conscious request (Emma Wilson)")
    print("6. ✅ Vague request needing clarification (Alex)")
    print("7. ✅ Special accessibility needs (Robert Martinez)")
    print("8. ✅ Corporate group booking (Sarah Chen)")
    print("9. ✅ Generic inquiry (Patricia Williams)")
    print("10. ✅ Spam email (should be ignored)")
    print()
    print("🔬 Expected NLP behavior:")
    print("- Scenarios 1-5,7-8: Should extract parameters and check availability")
    print("- Scenario 6: Should request clarification")  
    print("- Scenario 9: Should send generic reply")
    print("- Scenario 10: Should be ignored as spam")


if __name__ == "__main__":
    main() 