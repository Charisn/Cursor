"""Main NLP agent workflow orchestration."""

import time
from typing import List, Optional

from .config import get_settings
from .email_parser import EmailFetcher
from .intent_classifier import IntentClassifier
from .parameter_extractor import ParameterExtractor
from .edge_cases import EdgeCaseHandler
from .models import (
    EmailMessage,
    IntentType,
    NextAction,
    NLPProcessingResult,
    RoomRequest
)


class NLPAgent:
    """Main NLP agent that orchestrates the email processing pipeline."""
    
    def __init__(self):
        """Initialize NLP agent with all components."""
        self.settings = get_settings()
        
        # Initialize components
        self.email_fetcher = EmailFetcher()
        self.intent_classifier = IntentClassifier()
        self.parameter_extractor = ParameterExtractor()
        self.edge_case_handler = EdgeCaseHandler()
    
    def process_email(self, email: EmailMessage) -> NLPProcessingResult:
        """Process a single email through the complete NLP pipeline."""
        start_time = time.time()
        
        try:
            # Step 1: Classify intent
            intent_result = self.intent_classifier.classify_intent(email)
            
            # Step 2: Handle different intents
            if intent_result.intent == IntentType.IGNORE:
                return NLPProcessingResult(
                    intent=IntentType.IGNORE,
                    params=None,
                    confidence=intent_result.confidence,
                    next_action=NextAction.IGNORE_EMAIL,
                    processing_time_ms=(time.time() - start_time) * 1000
                )
            
            elif intent_result.intent == IntentType.GENERIC_QUERY:
                return NLPProcessingResult(
                    intent=IntentType.GENERIC_QUERY,
                    params=None,
                    confidence=intent_result.confidence,
                    next_action=NextAction.SEND_GENERIC_REPLY,
                    processing_time_ms=(time.time() - start_time) * 1000
                )
            
            elif intent_result.intent == IntentType.AVAILABILITY_REQUEST:
                # Step 3: Extract parameters for availability requests
                extraction_result = self.parameter_extractor.extract_parameters(email)
                
                # Step 4: Handle edge cases and determine next action
                edge_case_result = self.edge_case_handler.handle_availability_request(
                    email, extraction_result
                )
                
                # Calculate overall confidence
                overall_confidence = min(intent_result.confidence, extraction_result.confidence)
                
                return NLPProcessingResult(
                    intent=IntentType.AVAILABILITY_REQUEST,
                    params=extraction_result.params,
                    confidence=overall_confidence,
                    next_action=edge_case_result.next_action,
                    clarification_needed=edge_case_result.clarification_needed,
                    clarification_questions=edge_case_result.clarification_questions,
                    processing_time_ms=(time.time() - start_time) * 1000
                )
            
            else:
                # Fallback for unknown intents
                return NLPProcessingResult(
                    intent=IntentType.GENERIC_QUERY,
                    params=None,
                    confidence=0.5,
                    next_action=NextAction.SEND_GENERIC_REPLY,
                    processing_time_ms=(time.time() - start_time) * 1000
                )
                
        except Exception as e:
            # Handle any processing errors gracefully
            return NLPProcessingResult(
                intent=IntentType.GENERIC_QUERY,
                params=None,
                confidence=0.0,
                next_action=NextAction.SEND_GENERIC_REPLY,
                processing_time_ms=(time.time() - start_time) * 1000
            )
    
    def process_batch(self, emails: List[EmailMessage]) -> List[NLPProcessingResult]:
        """Process multiple emails in batch."""
        results = []
        
        for email in emails:
            result = self.process_email(email)
            results.append(result)
        
        return results
    
    def fetch_and_process_unread(self) -> List[NLPProcessingResult]:
        """Fetch unread emails and process them."""
        try:
            # Fetch unread emails
            emails = self.email_fetcher.fetch_unread_emails()
            
            # Process each email
            results = self.process_batch(emails)
            
            return results
            
        except Exception as e:
            print(f"Error fetching and processing emails: {e}")
            return []
    
    def get_processing_stats(self, results: List[NLPProcessingResult]) -> dict:
        """Get processing statistics for a batch of results."""
        if not results:
            return {}
        
        total_count = len(results)
        intent_counts = {}
        action_counts = {}
        avg_confidence = 0
        avg_processing_time = 0
        
        for result in results:
            # Count intents
            intent_key = result.intent.value
            intent_counts[intent_key] = intent_counts.get(intent_key, 0) + 1
            
            # Count actions
            action_key = result.next_action.value
            action_counts[action_key] = action_counts.get(action_key, 0) + 1
            
            # Sum confidence and processing time
            avg_confidence += result.confidence
            avg_processing_time += result.processing_time_ms
        
        # Calculate averages
        avg_confidence /= total_count
        avg_processing_time /= total_count
        
        return {
            "total_emails": total_count,
            "intent_distribution": intent_counts,
            "action_distribution": action_counts,
            "average_confidence": round(avg_confidence, 3),
            "average_processing_time_ms": round(avg_processing_time, 2),
            "clarification_needed_count": sum(1 for r in results if r.clarification_needed)
        }
    
    def is_healthy(self) -> bool:
        """Check if the NLP agent is healthy and ready to process emails."""
        try:
            # Test email fetcher connection
            with self.email_fetcher.connect() as client:
                client.list_folders()
            
            # Test Gemini connectivity (simplified)
            test_email = EmailMessage(
                subject="Test",
                body="Test email for health check",
                sender="test@example.com",
                received_at="2024-01-01T00:00:00Z",
                message_id="test-123"
            )
            
            # Try a quick classification
            result = self.intent_classifier.classify_intent(test_email)
            
            return result.confidence >= 0.0  # Basic sanity check
            
        except Exception:
            return False


class NLPWorkflow:
    """High-level workflow manager for NLP operations."""
    
    def __init__(self):
        """Initialize workflow manager."""
        self.agent = NLPAgent()
        self.settings = get_settings()
    
    def run_email_processing_cycle(self) -> dict:
        """Run a complete email processing cycle."""
        cycle_start = time.time()
        
        try:
            # Process unread emails
            results = self.agent.fetch_and_process_unread()
            
            # Get statistics
            stats = self.agent.get_processing_stats(results)
            
            # Add cycle timing
            stats["cycle_time_ms"] = (time.time() - cycle_start) * 1000
            stats["timestamp"] = time.time()
            
            return {
                "status": "success",
                "results": results,
                "stats": stats
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": time.time()
            }
    
    def process_single_email_text(self, subject: str, body: str, sender: str = "unknown@example.com") -> NLPProcessingResult:
        """Process a single email from raw text (useful for testing)."""
        email = EmailMessage(
            subject=subject,
            body=body,
            sender=sender,
            received_at=time.time(),
            message_id=f"manual-{int(time.time())}"
        )
        
        return self.agent.process_email(email)
    
    def health_check(self) -> dict:
        """Perform comprehensive health check."""
        return {
            "healthy": self.agent.is_healthy(),
            "timestamp": time.time(),
            "settings": {
                "confidence_threshold": self.settings.confidence_threshold,
                "max_processing_time": self.settings.max_processing_time,
                "gemini_model": self.settings.gemini_model
            }
        } 