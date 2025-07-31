
import asyncio
import json
import logging
import hashlib
import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import numpy as np
from sqlalchemy.orm import Session
from sklearn.ensemble import IsolationForest
from textblob import TextBlob
import difflib

from models.anti_cheat_alert import AntiCheatAlert, SuspicionLevel, ViolationType
from models.device_session import DeviceSession
from models.browser_activity import BrowserActivity
from models.clipboard_activity import ClipboardActivity
from models.ai_usage_detection import AIUsageDetection
from services.notification_service import NotificationService
from services.device_monitoring_service import DeviceMonitoringService
from utils.ml_models import BehaviorAnalysisModel, TextSimilarityModel
from config import settings

logger = logging.getLogger(__name__)

class CheatingPattern(str, Enum):
    DIRECT_COPY_PASTE = "direct_copy_paste"
    AI_GENERATED_CONTENT = "ai_generated_content"
    EXTERNAL_AI_USAGE = "external_ai_usage"
    RAPID_COMPLETION = "rapid_completion"
    UNUSUAL_VOCABULARY = "unusual_vocabulary"
    PERFECT_ANSWERS = "perfect_answers"
    BROWSER_SEARCHING = "browser_searching"
    PRIVATE_BROWSING = "private_browsing"
    VPN_USAGE = "vpn_usage"
    TIME_ANOMALY = "time_anomaly"
    BEHAVIOR_CHANGE = "behavior_change"

@dataclass
class SuspicionAlert:
    user_id: str
    pattern: CheatingPattern
    confidence: float
    evidence: Dict[str, Any]
    severity: SuspicionLevel
    recommended_action: str
    timestamp: datetime
    context: Dict[str, Any]

class AntiCheatService:
    """
    Mrs-Unkwn Anti-Cheat Engine - Intelligent detection of academic dishonesty
    
    This service monitors various signals to detect potential cheating while
    maintaining student privacy and providing educational guidance.
    """
    
    def __init__(self, db: Session = None):
        self.db = db
        self.notification_service = NotificationService()
        self.device_monitoring = DeviceMonitoringService()
        self.behavior_model = BehaviorAnalysisModel()
        self.text_similarity_model = TextSimilarityModel()
        
        # Known AI services and their patterns
        self.ai_services = {
            "chatgpt": ["chat.openai.com", "openai.com", "chatgpt"],
            "claude": ["claude.ai", "anthropic.com"],
            "bard": ["bard.google.com", "gemini.google.com"],
            "bing": ["bing.com/chat", "copilot.microsoft.com"],
            "perplexity": ["perplexity.ai"],
            "character_ai": ["character.ai", "c.ai"],
            "poe": ["poe.com"],
            "you_com": ["you.com"],
            "quillbot": ["quillbot.com"],
            "grammarly": ["grammarly.com"]
        }
        
        # Suspicious search patterns
        self.suspicious_patterns = [
            r"solve this (?:problem|equation|question)",
            r"(?:answer|solution) to (?:this|the) (?:problem|question|homework)",
            r"write (?:an?|my) essay (?:about|on|for)",
            r"complete (?:this|my) homework",
            r"do my assignment",
            r"solve for [a-zA-Z]",
            r"step by step solution",
            r"homework help",
            r"answer key",
            r"cheat sheet"
        ]
        
        # Compile regex patterns for efficiency
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.suspicious_patterns]
        
    async def analyze_interaction(
        self, 
        user_id: str, 
        message: str, 
        context: Dict[str, Any]
    ) -> bool:
        """Analyze a single AI interaction for cheating indicators"""
        try:
            alerts = []
            
            # 1. Analyze message content for direct solution requests
            content_alert = await self._analyze_message_content(user_id, message, context)
            if content_alert:
                alerts.append(content_alert)
            
            # 2. Check timing patterns
            timing_alert = await self._analyze_timing_patterns(user_id, context)
            if timing_alert:
                alerts.append(timing_alert)
            
            # 3. Check for copy-paste behavior
            clipboard_alert = await self._check_clipboard_activity(user_id, message, context)
            if clipboard_alert:
                alerts.append(clipboard_alert)
            
            # 4. Analyze vocabulary and complexity
            vocab_alert = await self._analyze_vocabulary_complexity(user_id, message, context)
            if vocab_alert:
                alerts.append(vocab_alert)
            
            # 5. Check concurrent browser activity
            browser_alert = await self._check_concurrent_browser_activity(user_id, context)
            if browser_alert:
                alerts.append(browser_alert)
            
            # Process alerts
            is_suspicious = False
            for alert in alerts:
                if alert.confidence > 0.7:
                    is_suspicious = True
                    await self._handle_suspicion_alert(alert)
                elif alert.confidence > 0.4:
                    await self._log_minor_suspicion(alert)
            
            return is_suspicious
            
        except Exception as e:
            logger.error(f"Error analyzing interaction: {str(e)}")
            return False
    
    async def _analyze_message_content(
        self, 
        user_id: str, 
        message: str, 
        context: Dict[str, Any]
    ) -> Optional[SuspicionAlert]:
        """Analyze message content for direct solution requests"""
        try:
            message_lower = message.lower()
            
            # Check for direct answer requests
            direct_requests = [
                "what is the answer", "give me the answer", "tell me the solution",
                "what's the correct answer", "just tell me", "solve this for me",
                "do this homework", "complete this assignment", "write this essay"
            ]
            
            direct_request_score = sum(1 for phrase in direct_requests if phrase in message_lower)
            
            # Check for suspicious patterns using regex
            pattern_matches = sum(1 for pattern in self.compiled_patterns if pattern.search(message))
            
            # Analyze question structure
            question_marks = message.count('?')
            exclamation_marks = message.count('!')
            
            # Check for homework-specific language
            homework_indicators = ["homework", "assignment", "due tomorrow", "test tomorrow", "quiz"]
            homework_score = sum(1 for indicator in homework_indicators if indicator in message_lower)
            
            # Calculate overall suspicion score
            suspicion_score = 0.0
            
            if direct_request_score > 0:
                suspicion_score += 0.4 * direct_request_score
            
            if pattern_matches > 0:
                suspicion_score += 0.3 * pattern_matches
                
            if homework_score > 0:
                suspicion_score += 0.2 * homework_score
            
            # Contextual factors
            if context.get("time_of_day", 12) > 22:  # Late night
                suspicion_score += 0.1
                
            if context.get("session_duration", 0) < 5:  # Very short session
                suspicion_score += 0.1
            
            # Normalize score
            suspicion_score = min(1.0, suspicion_score)
            
            if suspicion_score > 0.3:
                return SuspicionAlert(
                    user_id=user_id,
                    pattern=CheatingPattern.AI_GENERATED_CONTENT,
                    confidence=suspicion_score,
                    evidence={
                        "message": message[:200],  # Truncate for privacy
                        "direct_requests": direct_request_score,
                        "pattern_matches": pattern_matches,
                        "homework_indicators": homework_score,
                        "message_length": len(message)
                    },
                    severity=self._determine_severity(suspicion_score),
                    recommended_action=self._recommend_action(suspicion_score),
                    timestamp=datetime.utcnow(),
                    context=context
                )
            
            return None
            
        except Exception as e:
            logger.error(f"Error analyzing message content: {str(e)}")
            return None
    
    async def _analyze_timing_patterns(
        self, 
        user_id: str, 
        context: Dict[str, Any]
    ) -> Optional[SuspicionAlert]:
        """Analyze timing patterns for anomalies"""
        try:
            # Get recent interaction history
            recent_interactions = await self._get_recent_interactions(user_id, hours=24)
            
            if len(recent_interactions) < 3:
                return None
            
            # Calculate interaction intervals
            intervals = []
            for i in range(1, len(recent_interactions)):
                interval = (recent_interactions[i]['timestamp'] - recent_interactions[i-1]['timestamp']).total_seconds()
                intervals.append(interval)
            
            # Detect rapid-fire interactions (potential copy-paste)
            rapid_interactions = sum(1 for interval in intervals if interval < 30)  # 30 seconds
            
            # Detect unusual time patterns
            current_hour = datetime.utcnow().hour
            late_night_score = 1.0 if 23 <= current_hour or current_hour <= 5 else 0.0
            
            # Calculate suspicion based on timing
            timing_suspicion = 0.0
            
            if rapid_interactions > 2:
                timing_suspicion += 0.3 * (rapid_interactions / len(intervals))
            
            timing_suspicion += late_night_score * 0.2
            
            if timing_suspicion > 0.3:
                return SuspicionAlert(
                    user_id=user_id,
                    pattern=CheatingPattern.RAPID_COMPLETION,
                    confidence=timing_suspicion,
                    evidence={
                        "rapid_interactions": rapid_interactions,
                        "total_intervals": len(intervals),
                        "current_hour": current_hour,
                        "average_interval": np.mean(intervals) if intervals else 0
                    },
                    severity=self._determine_severity(timing_suspicion),
                    recommended_action="Monitor for rapid completion patterns",
                    timestamp=datetime.utcnow(),
                    context=context
                )
            
            return None
            
        except Exception as e:
            logger.error(f"Error analyzing timing patterns: {str(e)}")
            return None
    
    async def _check_clipboard_activity(
        self, 
        user_id: str, 
        message: str, 
        context: Dict[str, Any]
    ) -> Optional[SuspicionAlert]:
        """Check for suspicious clipboard activity"""
        try:
            # Get recent clipboard activity
            recent_clipboard = await self.db.query(ClipboardActivity).filter(
                ClipboardActivity.user_id == user_id,
                ClipboardActivity.timestamp >= datetime.utcnow() - timedelta(minutes=10)
            ).order_by(ClipboardActivity.timestamp.desc()).limit(10).all()
            
            if not recent_clipboard:
                return None
            
            # Check for large text copies
            large_copies = [clip for clip in recent_clipboard if len(clip.content_preview) > 100]
            
            # Check for external source copies
            external_copies = [clip for clip in recent_clipboard if clip.source_app not in ["Mrs-Unkwn", "internal"]]
            
            # Check message similarity to clipboard content
            similarity_scores = []
            for clip in recent_clipboard:
                if clip.content_preview:
                    similarity = self._calculate_text_similarity(message, clip.content_preview)
                    similarity_scores.append(similarity)
            
            max_similarity = max(similarity_scores) if similarity_scores else 0.0
            
            # Calculate suspicion score
            clipboard_suspicion = 0.0
            
            if len(large_copies) > 0:
                clipboard_suspicion += 0.3
            
            if len(external_copies) > 0:
                clipboard_suspicion += 0.4
            
            if max_similarity > 0.7:
                clipboard_suspicion += 0.5 * max_similarity
            
            if clipboard_suspicion > 0.3:
                return SuspicionAlert(
                    user_id=user_id,
                    pattern=CheatingPattern.DIRECT_COPY_PASTE,
                    confidence=clipboard_suspicion,
                    evidence={
                        "large_copies": len(large_copies),
                        "external_copies": len(external_copies),
                        "max_similarity": max_similarity,
                        "total_clipboard_events": len(recent_clipboard)
                    },
                    severity=self._determine_severity(clipboard_suspicion),
                    recommended_action="Investigate copy-paste behavior",
                    timestamp=datetime.utcnow(),
                    context=context
                )
            
            return None
            
        except Exception as e:
            logger.error(f"Error checking clipboard activity: {str(e)}")
            return None
    
    async def _analyze_vocabulary_complexity(
        self, 
        user_id: str, 
        message: str, 
        context: Dict[str, Any]
    ) -> Optional[SuspicionAlert]:
        """Analyze vocabulary complexity for anomalies"""
        try:
            # Get user's typical vocabulary level
            user_history = await self._get_user_message_history(user_id, limit=50)
            
            if len(user_history) < 10:
                return None  # Not enough data
            
            # Analyze current message
            current_analysis = self._analyze_text_complexity(message)
            
            # Analyze historical messages
            historical_analyses = [self._analyze_text_complexity(msg) for msg in user_history]
            
            # Calculate averages
            avg_complexity = np.mean([analysis['complexity_score'] for analysis in historical_analyses])
            avg_vocabulary_level = np.mean([analysis['vocabulary_level'] for analysis in historical_analyses])
            avg_sentence_length = np.mean([analysis['avg_sentence_length'] for analysis in historical_analyses])
            
            # Check for significant deviations
            complexity_deviation = (current_analysis['complexity_score'] - avg_complexity) / max(avg_complexity, 0.1)
            vocab_deviation = (current_analysis['vocabulary_level'] - avg_vocabulary_level) / max(avg_vocabulary_level, 0.1)
            length_deviation = (current_analysis['avg_sentence_length'] - avg_sentence_length) / max(avg_sentence_length, 0.1)
            
            # Calculate suspicion score
            vocab_suspicion = 0.0
            
            if complexity_deviation > 1.5:  # 150% higher than normal
                vocab_suspicion += 0.3
            
            if vocab_deviation > 2.0:  # 200% higher vocabulary level
                vocab_suspicion += 0.4
            
            if length_deviation > 1.5 and current_analysis['avg_sentence_length'] > 20:
                vocab_suspicion += 0.2
            
            # Check for AI-typical patterns
            ai_patterns = self._detect_ai_patterns(message)
            if ai_patterns['score'] > 0.5:
                vocab_suspicion += 0.3 * ai_patterns['score']
            
            if vocab_suspicion > 0.3:
                return SuspicionAlert(
                    user_id=user_id,
                    pattern=CheatingPattern.UNUSUAL_VOCABULARY,
                    confidence=vocab_suspicion,
                    evidence={
                        "complexity_deviation": complexity_deviation,
                        "vocab_deviation": vocab_deviation,
                        "length_deviation": length_deviation,
                        "current_complexity": current_analysis['complexity_score'],
                        "average_complexity": avg_complexity,
                        "ai_patterns": ai_patterns
                    },
                    severity=self._determine_severity(vocab_suspicion),
                    recommended_action="Review vocabulary complexity anomaly",
                    timestamp=datetime.utcnow(),
                    context=context
                )
            
            return None
            
        except Exception as e:
            logger.error(f"Error analyzing vocabulary complexity: {str(e)}")
            return None
    
    async def _check_concurrent_browser_activity(
        self, 
        user_id: str, 
        context: Dict[str, Any]
    ) -> Optional[SuspicionAlert]:
        """Check for concurrent browser activity during AI interaction"""
        try:
            # Get recent browser activity (last 5 minutes)
            recent_activity = await self.db.query(BrowserActivity).filter(
                BrowserActivity.user_id == user_id,
                BrowserActivity.timestamp >= datetime.utcnow() - timedelta(minutes=5)
            ).order_by(BrowserActivity.timestamp.desc()).limit(20).all()
            
            if not recent_activity:
                return None
            
            browser_suspicion = 0.0
            suspicious_activities = []
            
            for activity in recent_activity:
                # Check for AI service usage
                for service_name, domains in self.ai_services.items():
                    if any(domain in activity.url.lower() for domain in domains):
                        browser_suspicion += 0.5
                        suspicious_activities.append(f"Visited {service_name}")
                        break
                
                # Check for search engines with suspicious queries
                if any(search_engine in activity.url.lower() for search_engine in ["google.com/search", "bing.com/search", "duckduckgo.com"]):
                    if any(pattern.search(activity.url) for pattern in self.compiled_patterns):
                        browser_suspicion += 0.3
                        suspicious_activities.append("Suspicious search query")
                
                # Check for private browsing
                if activity.is_private_mode:
                    browser_suspicion += 0.2
                    suspicious_activities.append("Private browsing detected")
                
                # Check for homework help sites
                homework_sites = ["chegg.com", "coursehero.com", "studyblue.com", "quizlet.com", "slader.com"]
                if any(site in activity.url.lower() for site in homework_sites):
                    browser_suspicion += 0.4
                    suspicious_activities.append("Homework help site visited")
            
            if browser_suspicion > 0.3:
                return SuspicionAlert(
                    user_id=user_id,
                    pattern=CheatingPattern.EXTERNAL_AI_USAGE,
                    confidence=min(1.0, browser_suspicion),
                    evidence={
                        "suspicious_activities": suspicious_activities,
                        "total_browser_events": len(recent_activity),
                        "private_browsing_events": len([a for a in recent_activity if a.is_private_mode]),
                        "ai_service_visits": len([a for a in recent_activity if any(
                            any(domain in a.url.lower() for domain in domains) 
                            for domains in self.ai_services.values()
                        )])
                    },
                    severity=self._determine_severity(browser_suspicion),
                    recommended_action="Block external AI services and notify parents",
                    timestamp=datetime.utcnow(),
                    context=context
                )
            
            return None
            
        except Exception as e:
            logger.error(f"Error checking browser activity: {str(e)}")
            return None
    
    async def handle_suspicious_activity(
        self, 
        user_id: str, 
        activity_type: str, 
        details: Dict[str, Any]
    ):
        """Handle detected suspicious activity"""
        try:
            # Create alert record
            alert = AntiCheatAlert(
                user_id=user_id,
                activity_type=activity_type,
                suspicion_level=SuspicionLevel.MEDIUM,
                details=details,
                timestamp=datetime.utcnow(),
                resolved=False
            )
            
            self.db.add(alert)
            await self.db.commit()
            
            # Notify parents
            await self.notification_service.notify_parents_of_suspicious_activity(
                user_id, activity_type, details
            )
            
            # Log for analytics
            logger.warning(f"Suspicious activity detected for user {user_id}: {activity_type}")
            
        except Exception as e:
            logger.error(f"Error handling suspicious activity: {str(e)}")
    
    def _analyze_text_complexity(self, text: str) -> Dict[str, Any]:
        """Analyze text complexity metrics"""
        try:
            blob = TextBlob(text)
            sentences = blob.sentences
            words = blob.words
            
            # Basic metrics
            word_count = len(words)
            sentence_count = len(sentences)
            avg_sentence_length = word_count / max(sentence_count, 1)
            
            # Vocabulary complexity
            unique_words = len(set(word.lower() for word in words))
            vocabulary_richness = unique_words / max(word_count, 1)
            
            # Advanced vocabulary detection
            complex_words = sum(1 for word in words if len(word) > 6)
            complex_word_ratio = complex_words / max(word_count, 1)
            
            # Calculate overall complexity score
            complexity_score = (
                min(avg_sentence_length / 15, 1.0) * 0.3 +
                vocabulary_richness * 0.4 +
                complex_word_ratio * 0.3
            )
            
            return {
                "word_count": word_count,
                "sentence_count": sentence_count,
                "avg_sentence_length": avg_sentence_length,
                "vocabulary_richness": vocabulary_richness,
                "complex_word_ratio": complex_word_ratio,
                "complexity_score": complexity_score,
                "vocabulary_level": self._estimate_vocabulary_level(words)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing text complexity: {str(e)}")
            return {
                "complexity_score": 0.5,
                "vocabulary_level": 5,
                "avg_sentence_length": len(text.split()) / max(text.count('.'), 1)
            }
    
    def _detect_ai_patterns(self, text: str) -> Dict[str, Any]:
        """Detect patterns typical of AI-generated text"""
        ai_indicators = {
            "formal_structure": 0,
            "perfect_grammar": 0,
            "academic_language": 0,
            "consistent_tone": 0,
            "lack_of_personality": 0
        }
        
        text_lower = text.lower()
        
        # Check for overly formal structure
        formal_phrases = ["furthermore", "moreover", "nevertheless", "consequently", "thus", "therefore"]
        ai_indicators["formal_structure"] = sum(1 for phrase in formal_phrases if phrase in text_lower) / 10
        
        # Check for academic language patterns
        academic_words = ["utilize", "facilitate", "demonstrate", "implement", "comprehensive", "fundamental"]
        ai_indicators["academic_language"] = sum(1 for word in academic_words if word in text_lower) / 10
        
        # Simple pattern detection
        sentences = text.split('.')
        if len(sentences) > 1:
            # Check for consistent sentence length (AI tends to be consistent)
            lengths = [len(s.split()) for s in sentences if s.strip()]
            if lengths:
                length_variance = np.var(lengths)
                ai_indicators["consistent_tone"] = 1.0 if length_variance < 5 else 0.0
        
        # Calculate overall AI pattern score
        ai_score = sum(ai_indicators.values()) / len(ai_indicators)
        
        return {
            "score": min(1.0, ai_score),
            "indicators": ai_indicators
        }
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts"""
        try:
            # Use difflib for basic similarity
            similarity = difflib.SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
            return similarity
        except Exception:
            return 0.0
    
    def _estimate_vocabulary_level(self, words: List[str]) -> int:
        """Estimate vocabulary level (1-10 scale)"""
        try:
            # Simple heuristic based on word length and complexity
            avg_word_length = np.mean([len(word) for word in words])
            long_words = sum(1 for word in words if len(word) > 7)
            long_word_ratio = long_words / max(len(words), 1)
            
            # Estimate level
            level = min(10, max(1, int(
                avg_word_length * 1.2 + long_word_ratio * 8
            )))
            
            return level
        except Exception:
            return 5
    
    def _determine_severity(self, confidence: float) -> SuspicionLevel:
        """Determine severity level based on confidence"""
        if confidence >= 0.8:
            return SuspicionLevel.HIGH
        elif confidence >= 0.5:
            return SuspicionLevel.MEDIUM
        else:
            return SuspicionLevel.LOW
    
    def _recommend_action(self, confidence: float) -> str:
        """Recommend action based on confidence level"""
        if confidence >= 0.8:
            return "Immediate parent notification and session pause"
        elif confidence >= 0.6:
            return "Parent notification and increased monitoring"
        elif confidence >= 0.4:
            return "Log for review and monitor closely"
        else:
            return "Continue monitoring"
    
    async def _get_recent_interactions(self, user_id: str, hours: int = 24) -> List[Dict[str, Any]]:
        """Get recent AI interactions for pattern analysis"""
        try:
            # This would query the AI interaction history
            # Placeholder implementation
            return []
        except Exception as e:
            logger.error(f"Error getting recent interactions: {str(e)}")
            return []
    
    async def _get_user_message_history(self, user_id: str, limit: int = 50) -> List[str]:
        """Get user's message history for analysis"""
        try:
            # This would query the user's message history
            # Placeholder implementation
            return []
        except Exception as e:
            logger.error(f"Error getting message history: {str(e)}")
            return []
    
    async def _handle_suspicion_alert(self, alert: SuspicionAlert):
        """Handle a suspicion alert"""
        try:
            # Save to database
            db_alert = AntiCheatAlert(
                user_id=alert.user_id,
                activity_type=alert.pattern.value,
                suspicion_level=alert.severity,
                details=alert.evidence,
                timestamp=alert.timestamp,
                resolved=False
            )
            
            self.db.add(db_alert)
            await self.db.commit()
            
            # Notify based on severity
            if alert.severity == SuspicionLevel.HIGH:
                await self.notification_service.send_immediate_parent_alert(
                    alert.user_id, alert.pattern.value, alert.evidence
                )
            elif alert.severity == SuspicionLevel.MEDIUM:
                await self.notification_service.send_parent_notification(
                    alert.user_id, alert.pattern.value, alert.evidence
                )
            
            logger.warning(f"Suspicion alert handled: {alert.pattern.value} for user {alert.user_id}")
            
        except Exception as e:
            logger.error(f"Error handling suspicion alert: {str(e)}")
    
    async def _log_minor_suspicion(self, alert: SuspicionAlert):
        """Log minor suspicion for pattern tracking"""
        try:
            # Log to a separate table for pattern analysis
            logger.info(f"Minor suspicion logged: {alert.pattern.value} for user {alert.user_id} (confidence: {alert.confidence})")
        except Exception as e:
            logger.error(f"Error logging minor suspicion: {str(e)}")
    
    async def get_active_alerts(self, session_id: str) -> List[AntiCheatAlert]:
        """Get active alerts for a session"""
        try:
            alerts = await self.db.query(AntiCheatAlert).filter(
                AntiCheatAlert.session_id == session_id,
                AntiCheatAlert.resolved == False,
                AntiCheatAlert.timestamp >= datetime.utcnow() - timedelta(hours=24)
            ).all()
            
            return alerts
        except Exception as e:
            logger.error(f"Error getting active alerts: {str(e)}")
            return []
