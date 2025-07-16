#!/usr/bin/env python3
"""CLI tool for testing NLP functionality."""

import argparse
import json
import sys
from datetime import datetime

from src.agent_workflow import NLPWorkflow


def test_email_processing(subject: str, body: str, sender: str = "test@example.com"):
    """Test email processing with given content."""
    print("🔄 Initializing NLP workflow...")
    
    try:
        workflow = NLPWorkflow()
        print("✅ NLP workflow initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize NLP workflow: {e}")
        return False
    
    print(f"\n📧 Processing email:")
    print(f"From: {sender}")
    print(f"Subject: {subject}")
    print(f"Body: {body[:100]}{'...' if len(body) > 100 else ''}")
    print("-" * 50)
    
    try:
        result = workflow.process_single_email_text(subject, body, sender)
        
        print(f"\n📊 Processing Results:")
        print(f"Intent: {result.intent}")
        print(f"Confidence: {result.confidence:.3f}")
        print(f"Next Action: {result.next_action}")
        print(f"Processing Time: {result.processing_time_ms:.2f}ms")
        
        if result.params:
            print(f"\n📋 Extracted Parameters:")
            if result.params.date:
                print(f"  Date: {result.params.date}")
            if result.params.room_count:
                print(f"  Room Count: {result.params.room_count}")
            if result.params.budget:
                print(f"  Budget: ${result.params.budget}")
            if result.params.view_preference:
                print(f"  View Preference: {result.params.view_preference}")
            if result.params.special_requests:
                print(f"  Special Requests: {result.params.special_requests}")
        
        if result.clarification_needed:
            print(f"\n❓ Clarification Questions:")
            for question in result.clarification_questions:
                print(f"  • {question}")
        
        return True
        
    except Exception as e:
        print(f"❌ Processing failed: {e}")
        return False


def test_health_check():
    """Test NLP service health."""
    print("🔄 Running health check...")
    
    try:
        workflow = NLPWorkflow()
        health = workflow.health_check()
        
        if health["healthy"]:
            print("✅ NLP service is healthy")
            print(f"Settings: {json.dumps(health['settings'], indent=2)}")
        else:
            print("❌ NLP service is unhealthy")
        
        return health["healthy"]
        
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False


def run_sample_tests():
    """Run predefined sample tests."""
    samples = [
        {
            "subject": "Room Availability",
            "body": "Hi, I need 2 rooms for December 25th, 2024. My budget is around $150 per room with ocean view if possible.",
            "sender": "john.doe@example.com"
        },
        {
            "subject": "Booking inquiry",
            "body": "Hello, do you have any availability for next Friday? I need 1 room.",
            "sender": "mary@test.com"
        },
        {
            "subject": "General question",
            "body": "What time is check-in? Also, do you have a pool?",
            "sender": "guest@hotel.com"
        },
        {
            "subject": "Spam email",
            "body": "URGENT! You've won $1000000! Click here now!!!",
            "sender": "spam@badactor.com"
        }
    ]
    
    print(f"🧪 Running {len(samples)} sample tests...\n")
    
    for i, sample in enumerate(samples, 1):
        print(f"Test {i}/{len(samples)}")
        success = test_email_processing(
            sample["subject"],
            sample["body"],
            sample["sender"]
        )
        
        if i < len(samples):
            print("\n" + "="*70 + "\n")
    
    print("🏁 Sample tests completed!")


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(description="Test Staydesk NLP functionality")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Health check command
    subparsers.add_parser("health", help="Run health check")
    
    # Process email command
    process_parser = subparsers.add_parser("process", help="Process a single email")
    process_parser.add_argument("--subject", required=True, help="Email subject")
    process_parser.add_argument("--body", required=True, help="Email body")
    process_parser.add_argument("--sender", default="test@example.com", help="Sender email")
    
    # Sample tests command
    subparsers.add_parser("samples", help="Run predefined sample tests")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    print("🏨 Staydesk NLP Testing Tool")
    print("=" * 40)
    
    if args.command == "health":
        success = test_health_check()
        sys.exit(0 if success else 1)
    
    elif args.command == "process":
        success = test_email_processing(args.subject, args.body, args.sender)
        sys.exit(0 if success else 1)
    
    elif args.command == "samples":
        run_sample_tests()
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main() 