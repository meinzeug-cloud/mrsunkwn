
import asyncio
import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import openai
from openai import AsyncOpenAI
import redis
from sqlalchemy.orm import Session

from models.ai_interaction import AIInteraction, InteractionType, SocraticLevel
from models.learning_session import LearningSession
from models.user_profile import UserProfile
from services.learning_analytics_service import LearningAnalyticsService
from services.content_service import ContentService
from utils.pedagogy import SocraticMethodEngine, HintGenerationEngine
from config import settings

logger = logging.getLogger(__name__)

class TutorPersonality(str, Enum):
    ENCOURAGING = "encouraging"
    CHALLENGING = "challenging"
    PATIENT = "patient"
    ENTHUSIASTIC = "enthusiastic"

class LearningObjective(str, Enum):
    UNDERSTANDING = "understanding"
    PROBLEM_SOLVING = "problem_solving"
    CRITICAL_THINKING = "critical_thinking"
    KNOWLEDGE_APPLICATION = "knowledge_application"
    CREATIVE_EXPRESSION = "creative_expression"

@dataclass
class SocraticResponse:
    message: str
    questions: List[str]
    hints: List[str]
    follow_up_prompts: List[str]
    difficulty_adjustment: int
    learning_objective: LearningObjective
    confidence_score: float
    next_steps: List[str]

class AITutorService:
    """
    Mrs-Unkwn AI Tutor Service - Implements Socratic Method for personalized learning
    
    This service provides intelligent tutoring that guides students to discover
    solutions themselves rather than providing direct answers.
    """
    
    def __init__(self, db: Session = None):
        self.db = db
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.redis_client = redis.from_url(settings.REDIS_URL)
        self.socratic_engine = SocraticMethodEngine()
        self.hint_engine = HintGenerationEngine()
        self.analytics_service = LearningAnalyticsService(db)
        self.content_service = ContentService(db)
        
        # AI Model configuration for Mrs-Unkwn
        self.model_config = {
            "model": "gpt-4-turbo-preview",
            "temperature": 0.7,
            "max_tokens": 1000,
            "top_p": 0.9
        }
        
    async def process_socratic_interaction(
        self, 
        item_id: str,
        user_message: str,
        user_id: str,
        apply_pedagogy: bool = True
    ) -> Dict[str, Any]:
        """Process user interaction using Socratic method"""
        try:
            # Get user context and learning history
            user_context = await self._get_user_learning_context(user_id, item_id)
            
            # Analyze the user's message for learning patterns
            message_analysis = await self._analyze_user_message(user_message, user_context)
            
            # Generate Socratic response based on pedagogy
            if apply_pedagogy:
                response = await self._generate_socratic_response(
                    user_message, 
                    user_context, 
                    message_analysis
                )
            else:
                response = await self._generate_standard_response(user_message, user_context)
            
            # Log interaction for analytics
            await self._log_ai_interaction(
                user_id, item_id, user_message, response, message_analysis
            )
            
            # Update learning progress
            await self._update_learning_progress(user_id, item_id, response)
            
            return {
                "response": response.message,
                "type": "socratic_guidance",
                "questions": response.questions,
                "hints": response.hints[:2] if response.hints else [],  # Limit hints
                "learning_objective": response.learning_objective.value,
                "confidence_score": response.confidence_score,
                "next_steps": response.next_steps,
                "difficulty_level": user_context.get("difficulty_level", 5),
                "interaction_id": await self._generate_interaction_id()
            }
            
        except Exception as e:
            logger.error(f"Error in Socratic interaction: {str(e)}")
            return await self._generate_fallback_response(user_message)
    
    async def _get_user_learning_context(self, user_id: str, item_id: str) -> Dict[str, Any]:
        """Get comprehensive user learning context"""
        try:
            # Get user profile and preferences
            user_profile = await self.db.query(UserProfile).filter(
                UserProfile.user_id == user_id
            ).first()
            
            # Get recent learning session data
            recent_sessions = await self.analytics_service.get_recent_sessions(
                user_id, limit=10
            )
            
            # Get current learning session details
            current_session = await self.db.query(LearningSession).filter(
                LearningSession.id == item_id
            ).first()
            
            # Analyze learning patterns
            learning_patterns = await self.analytics_service.analyze_learning_patterns(
                user_id, timeframe="week"
            )
            
            context = {
                "user_id": user_id,
                "age": user_profile.age if user_profile else 15,
                "learning_style": user_profile.learning_style if user_profile else "visual",
                "difficulty_preference": user_profile.difficulty_preference if user_profile else 5,
                "subject_areas": current_session.subject_areas if current_session else [],
                "current_topic": current_session.current_topic if current_session else "general",
                "session_duration": (datetime.utcnow() - current_session.started_at).total_seconds() / 60 if current_session else 0,
                "recent_performance": learning_patterns.get("average_score", 0.7),
                "struggle_areas": learning_patterns.get("struggle_areas", []),
                "strength_areas": learning_patterns.get("strength_areas", []),
                "learning_velocity": learning_patterns.get("learning_velocity", "normal"),
                "engagement_level": learning_patterns.get("engagement_level", "medium"),
                "question_asking_frequency": learning_patterns.get("question_frequency", "normal"),
                "hint_usage_pattern": learning_patterns.get("hint_usage", "balanced"),
                "last_interaction_time": learning_patterns.get("last_interaction", datetime.utcnow()),
                "preferred_explanation_style": user_profile.preferred_explanation_style if user_profile else "detailed"
            }
            
            return context
            
        except Exception as e:
            logger.error(f"Error getting user context: {str(e)}")
            return {"user_id": user_id, "age": 15, "difficulty_preference": 5}
    
    async def _analyze_user_message(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze user message for learning indicators"""
        try:
            analysis_prompt = f"""
            Analyze this student message in the context of Mrs-Unkwn AI tutoring:
            
            Student Message: "{message}"
            Student Context: Age {context.get('age', 15)}, Subject: {context.get('current_topic', 'general')}
            
            Analyze for:
            1. Confidence level (0.0-1.0)
            2. Understanding depth (surface/moderate/deep)
            3. Question type (clarification/help/verification/exploration)
            4. Emotional state (frustrated/confident/curious/overwhelmed)
            5. Learning readiness (ready/needs_support/needs_break)
            6. Misconceptions present (true/false + details)
            7. Prior knowledge indicators
            8. Engagement level (low/medium/high)
            
            Return JSON format with these fields.
            """
            
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are an expert educational psychologist analyzing student communications."},
                    {"role": "user", "content": analysis_prompt}
                ],
                temperature=0.3,
                max_tokens=300
            )
            
            analysis = json.loads(response.choices[0].message.content)
            
            # Add pattern matching analysis
            analysis.update(await self._pattern_match_message(message))
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing message: {str(e)}")
            return {
                "confidence_level": 0.5,
                "understanding_depth": "moderate",
                "question_type": "help",
                "emotional_state": "neutral",
                "learning_readiness": "ready"
            }
    
    async def _generate_socratic_response(
        self, 
        user_message: str, 
        context: Dict[str, Any], 
        analysis: Dict[str, Any]
    ) -> SocraticResponse:
        """Generate response using Socratic Method principles"""
        try:
            # Determine appropriate Socratic approach
            socratic_level = self._determine_socratic_level(analysis, context)
            
            # Build context-aware prompt for Socratic guidance
            socratic_prompt = await self._build_socratic_prompt(
                user_message, context, analysis, socratic_level
            )
            
            # Generate response using AI with Socratic constraints
            response = await self.client.chat.completions.create(
                model=self.model_config["model"],
                messages=[
                    {
                        "role": "system", 
                        "content": """You are Mrs-Unkwn, a friendly AI tutor for teenagers. You NEVER give direct answers. 
                        Instead, you guide students to discover solutions through questions, hints, and encouragement.
                        Use the Socratic method: ask thought-provoking questions that lead students to insights.
                        Be patient, encouraging, and age-appropriate for teenagers."""
                    },
                    {"role": "user", "content": socratic_prompt}
                ],
                **self.model_config
            )
            
            ai_response = response.choices[0].message.content
            
            # Parse and structure the response
            structured_response = await self._structure_socratic_response(
                ai_response, analysis, context
            )
            
            # Generate additional hints if needed
            if analysis.get("learning_readiness") == "needs_support":
                additional_hints = await self.hint_engine.generate_progressive_hints(
                    user_message, context["current_topic"], context["difficulty_preference"]
                )
                structured_response.hints.extend(additional_hints[:2])
            
            return structured_response
            
        except Exception as e:
            logger.error(f"Error generating Socratic response: {str(e)}")
            return await self._generate_fallback_socratic_response(user_message, context)
    
    async def _build_socratic_prompt(
        self, 
        user_message: str, 
        context: Dict[str, Any], 
        analysis: Dict[str, Any],
        socratic_level: SocraticLevel
    ) -> str:
        """Build context-aware prompt for Socratic method"""
        
        difficulty_guidance = {
            1: "Use very simple questions and concrete examples",
            2: "Use simple questions with gentle guidance", 
            3: "Use straightforward questions with some complexity",
            4: "Use moderately challenging questions",
            5: "Use balanced questions with good depth",
            6: "Use thoughtful questions that require analysis",
            7: "Use challenging questions that promote critical thinking",
            8: "Use complex questions that require synthesis",
            9: "Use advanced questions that require evaluation",
            10: "Use sophisticated questions that require creation and innovation"
        }
        
        emotional_guidance = {
            "frustrated": "Be extra patient and break down concepts into smaller steps",
            "overwhelmed": "Simplify and focus on one concept at a time",
            "confident": "Challenge appropriately and encourage deeper thinking",
            "curious": "Nurture curiosity with exploratory questions"
        }
        
        prompt = f"""
        Student said: "{user_message}"
        
        Context:
        - Age: {context.get('age', 15)}
        - Subject: {context.get('current_topic', 'general')}
        - Difficulty level: {context.get('difficulty_preference', 5)}/10
        - Learning style: {context.get('learning_style', 'visual')}
        - Session duration: {context.get('session_duration', 0):.1f} minutes
        
        Analysis:
        - Confidence: {analysis.get('confidence_level', 0.5)}
        - Understanding: {analysis.get('understanding_depth', 'moderate')}
        - Emotional state: {analysis.get('emotional_state', 'neutral')}
        - Question type: {analysis.get('question_type', 'help')}
        
        Guidance:
        - {difficulty_guidance.get(context.get('difficulty_preference', 5), 'Use appropriate level questions')}
        - {emotional_guidance.get(analysis.get('emotional_state', 'neutral'), 'Maintain supportive tone')}
        
        Socratic Method Instructions:
        1. NEVER give direct answers or solutions
        2. Ask 2-3 guiding questions that help the student think through the problem
        3. Provide gentle hints if the student seems stuck
        4. Encourage the student's thinking process
        5. Relate to their interests when possible
        6. Use analogies appropriate for teenagers
        7. Celebrate small victories and insights
        
        Generate a response that includes:
        - Main guidance message (encouraging, never giving answers)
        - 2-3 Socratic questions to guide thinking
        - 1-2 gentle hints if appropriate
        - Encouragement and next steps
        
        Keep the tone friendly, patient, and age-appropriate for teenagers.
        """
        
        return prompt
    
    async def _structure_socratic_response(
        self, 
        ai_response: str, 
        analysis: Dict[str, Any], 
        context: Dict[str, Any]
    ) -> SocraticResponse:
        """Structure AI response into Socratic components"""
        try:
            # Parse the AI response to extract components
            lines = ai_response.split('\n')
            
            main_message = []
            questions = []
            hints = []
            
            current_section = "message"
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                if any(indicator in line.lower() for indicator in ["question:", "ask yourself:", "think about:"]):
                    current_section = "questions"
                    questions.append(line.replace("Question:", "").replace("Ask yourself:", "").strip())
                elif any(indicator in line.lower() for indicator in ["hint:", "tip:", "consider:"]):
                    current_section = "hints"
                    hints.append(line.replace("Hint:", "").replace("Tip:", "").strip())
                elif line.endswith("?"):
                    questions.append(line)
                elif current_section == "message":
                    main_message.append(line)
                elif current_section == "questions":
                    questions.append(line)
                elif current_section == "hints":
                    hints.append(line)
            
            # Determine learning objective based on context
            learning_objective = self._determine_learning_objective(analysis, context)
            
            # Calculate confidence score
            confidence_score = self._calculate_response_confidence(analysis, context)
            
            # Generate next steps
            next_steps = await self._generate_next_steps(analysis, context)
            
            # Determine difficulty adjustment
            difficulty_adjustment = self._calculate_difficulty_adjustment(analysis, context)
            
            return SocraticResponse(
                message=" ".join(main_message) if main_message else ai_response,
                questions=questions[:3],  # Limit to 3 questions
                hints=hints[:2],  # Limit to 2 hints
                follow_up_prompts=await self._generate_follow_up_prompts(context),
                difficulty_adjustment=difficulty_adjustment,
                learning_objective=learning_objective,
                confidence_score=confidence_score,
                next_steps=next_steps
            )
            
        except Exception as e:
            logger.error(f"Error structuring Socratic response: {str(e)}")
            return SocraticResponse(
                message=ai_response,
                questions=[],
                hints=[],
                follow_up_prompts=[],
                difficulty_adjustment=0,
                learning_objective=LearningObjective.UNDERSTANDING,
                confidence_score=0.5,
                next_steps=["Continue practicing", "Ask questions when stuck"]
            )
    
    async def _log_ai_interaction(
        self, 
        user_id: str, 
        item_id: str, 
        user_message: str, 
        response: SocraticResponse, 
        analysis: Dict[str, Any]
    ):
        """Log AI interaction for analytics and improvement"""
        try:
            interaction = AIInteraction(
                user_id=user_id,
                session_id=item_id,
                user_message=user_message,
                ai_response=response.message,
                interaction_type=InteractionType.SOCRATIC_GUIDANCE,
                confidence_score=response.confidence_score,
                learning_objective=response.learning_objective,
                questions_asked=len(response.questions),
                hints_provided=len(response.hints),
                difficulty_level=analysis.get("difficulty_level", 5),
                user_confidence=analysis.get("confidence_level", 0.5),
                emotional_state=analysis.get("emotional_state", "neutral"),
                timestamp=datetime.utcnow(),
                metadata={
                    "analysis": analysis,
                    "context_used": True,
                    "socratic_method": True,
                    "response_length": len(response.message)
                }
            )
            
            self.db.add(interaction)
            await self.db.commit()
            
        except Exception as e:
            logger.error(f"Error logging AI interaction: {str(e)}")
    
    async def initialize_for_learning_session(self, session_id: str) -> Dict[str, Any]:
        """Initialize AI tutor for a new learning session"""
        try:
            session = await self.db.query(LearningSession).filter(
                LearningSession.id == session_id
            ).first()
            
            if not session:
                raise ValueError("Learning session not found")
            
            # Create initial AI context
            initial_context = {
                "session_id": session_id,
                "subject": session.subject_areas[0] if session.subject_areas else "general",
                "difficulty_level": session.difficulty_level,
                "learning_objectives": session.learning_objectives or [],
                "ai_personality": session.ai_personality or TutorPersonality.ENCOURAGING,
                "initialized_at": datetime.utcnow()
            }
            
            # Store in Redis for fast access
            await self.redis_client.setex(
                f"ai_context:{session_id}",
                3600,  # 1 hour TTL
                json.dumps(initial_context, default=str)
            )
            
            # Generate welcome message
            welcome_message = await self._generate_welcome_message(session, initial_context)
            
            logger.info(f"AI Tutor initialized for session {session_id}")
            
            return {
                "initialized": True,
                "session_id": session_id,
                "welcome_message": welcome_message,
                "ai_personality": initial_context["ai_personality"],
                "available_features": [
                    "socratic_questioning",
                    "hint_generation", 
                    "progress_tracking",
                    "adaptive_difficulty",
                    "learning_analytics"
                ]
            }
            
        except Exception as e:
            logger.error(f"Error initializing AI tutor: {str(e)}")
            return {"initialized": False, "error": str(e)}
    
    async def _generate_welcome_message(self, session: LearningSession, context: Dict[str, Any]) -> str:
        """Generate personalized welcome message"""
        try:
            subject = context.get("subject", "learning")
            personality = context.get("ai_personality", "encouraging")
            
            personality_styles = {
                TutorPersonality.ENCOURAGING: "Hi there! I'm excited to learn {subject} with you today! 🌟",
                TutorPersonality.CHALLENGING: "Ready for an intellectual adventure in {subject}? Let's dive deep! 🧠",
                TutorPersonality.PATIENT: "Welcome! Take your time, and remember - every question is a great question in {subject}. 😊",
                TutorPersonality.ENTHUSIASTIC: "WOW! {subject} is going to be SO much fun today! Let's explore together! 🚀"
            }
            
            base_message = personality_styles.get(
                personality, 
                "Welcome! I'm here to help you discover amazing things about {subject}! 🎓"
            ).format(subject=subject)
            
            return f"{base_message} Remember, I won't give you direct answers - instead, I'll guide you to find them yourself. That's how real learning happens! What would you like to explore first?"
            
        except Exception as e:
            logger.error(f"Error generating welcome message: {str(e)}")
            return "Welcome! I'm your AI tutor, here to guide your learning journey. What shall we explore today?"
    
    def _determine_socratic_level(self, analysis: Dict[str, Any], context: Dict[str, Any]) -> SocraticLevel:
        """Determine appropriate level of Socratic questioning"""
        confidence = analysis.get("confidence_level", 0.5)
        understanding = analysis.get("understanding_depth", "moderate")
        age = context.get("age", 15)
        
        if confidence < 0.3 or understanding == "surface" or age < 14:
            return SocraticLevel.GENTLE
        elif confidence > 0.7 and understanding == "deep" and age > 16:
            return SocraticLevel.CHALLENGING
        else:
            return SocraticLevel.BALANCED
    
    def _determine_learning_objective(self, analysis: Dict[str, Any], context: Dict[str, Any]) -> LearningObjective:
        """Determine the primary learning objective for this interaction"""
        question_type = analysis.get("question_type", "help")
        understanding = analysis.get("understanding_depth", "moderate")
        
        if question_type == "exploration":
            return LearningObjective.CREATIVE_EXPRESSION
        elif question_type == "problem_solving":
            return LearningObjective.PROBLEM_SOLVING
        elif understanding == "surface":
            return LearningObjective.UNDERSTANDING
        elif understanding == "deep":
            return LearningObjective.CRITICAL_THINKING
        else:
            return LearningObjective.KNOWLEDGE_APPLICATION
    
    def _calculate_response_confidence(self, analysis: Dict[str, Any], context: Dict[str, Any]) -> float:
        """Calculate confidence score for the AI response"""
        user_confidence = analysis.get("confidence_level", 0.5)
        understanding = analysis.get("understanding_depth", "moderate")
        context_completeness = len(context) / 15  # Normalize context richness
        
        # Higher confidence when we have good context and user shows understanding
        base_confidence = 0.7
        confidence_adjustments = {
            "surface": -0.2,
            "moderate": 0.0,
            "deep": +0.2
        }
        
        confidence = base_confidence + confidence_adjustments.get(understanding, 0)
        confidence += (context_completeness - 0.5) * 0.2
        confidence += (user_confidence - 0.5) * 0.1
        
        return max(0.1, min(1.0, confidence))
    
    def _calculate_difficulty_adjustment(self, analysis: Dict[str, Any], context: Dict[str, Any]) -> int:
        """Calculate difficulty level adjustment (-2 to +2)"""
        confidence = analysis.get("confidence_level", 0.5)
        emotional_state = analysis.get("emotional_state", "neutral")
        understanding = analysis.get("understanding_depth", "moderate")
        
        adjustment = 0
        
        # Adjust based on confidence
        if confidence < 0.3:
            adjustment -= 1
        elif confidence > 0.8:
            adjustment += 1
        
        # Adjust based on emotional state
        if emotional_state in ["frustrated", "overwhelmed"]:
            adjustment -= 1
        elif emotional_state in ["confident", "curious"]:
            adjustment += 1
        
        # Adjust based on understanding
        if understanding == "surface":
            adjustment -= 1
        elif understanding == "deep":
            adjustment += 1
        
        return max(-2, min(2, adjustment))
    
    async def _generate_next_steps(self, analysis: Dict[str, Any], context: Dict[str, Any]) -> List[str]:
        """Generate personalized next steps for the student"""
        understanding = analysis.get("understanding_depth", "moderate")
        confidence = analysis.get("confidence_level", 0.5)
        emotional_state = analysis.get("emotional_state", "neutral")
        
        next_steps = []
        
        if understanding == "surface":
            next_steps.extend([
                "Take time to understand the basic concepts",
                "Ask questions about anything that seems unclear"
            ])
        elif understanding == "deep" and confidence > 0.7:
            next_steps.extend([
                "Try applying this concept to a different problem",
                "Think about how this connects to other topics you know"
            ])
        
        if emotional_state == "frustrated":
            next_steps.append("Take a short break if you need to - learning takes patience!")
        elif emotional_state == "curious":
            next_steps.append("Explore related topics that interest you")
        
        # Always include encouraging next steps
        next_steps.extend([
            "Keep asking great questions",
            "Celebrate your progress - you're doing well!"
        ])
        
        return next_steps[:3]  # Limit to 3 steps
    
    async def _generate_follow_up_prompts(self, context: Dict[str, Any]) -> List[str]:
        """Generate follow-up prompts to continue learning"""
        subject = context.get("current_topic", "this topic")
        
        prompts = [
            f"What else would you like to explore about {subject}?",
            f"How do you think {subject} connects to things you already know?",
            "What questions are coming to mind as we discuss this?",
            "Would you like to try a different approach to this problem?",
            "What part of this is most interesting to you?"
        ]
        
        return prompts[:2]  # Return 2 follow-up prompts
        
    async def _generate_fallback_response(self, user_message: str) -> Dict[str, Any]:
        """Generate fallback response when AI processing fails"""
        return {
            "response": "I'm having a bit of trouble right now, but let's keep learning together! Can you tell me more about what you're working on?",
            "type": "fallback",
            "questions": ["What specific part would you like help with?"],
            "hints": ["Sometimes breaking a problem into smaller parts can help"],
            "interaction_id": await self._generate_interaction_id()
        }
    
    async def _generate_interaction_id(self) -> str:
        """Generate unique interaction ID"""
        timestamp = int(datetime.utcnow().timestamp() * 1000)
        return f"ai_interaction_{timestamp}"
        
    async def _pattern_match_message(self, message: str) -> Dict[str, Any]:
        """Pattern match message for common indicators"""
        message_lower = message.lower()
        
        patterns = {
            "asking_for_answer": any(phrase in message_lower for phrase in [
                "what is the answer", "give me the answer", "tell me the solution",
                "what's the correct answer", "just tell me"
            ]),
            "showing_work": any(phrase in message_lower for phrase in [
                "i think", "my answer is", "i got", "i calculated", "i tried"
            ]),
            "asking_for_help": any(phrase in message_lower for phrase in [
                "help", "don't understand", "confused", "stuck", "how do i"
            ]),
            "expressing_frustration": any(phrase in message_lower for phrase in [
                "frustrated", "giving up", "too hard", "impossible", "hate this"
            ]),
            "showing_curiosity": any(phrase in message_lower for phrase in [
                "why", "how does", "what if", "curious", "interesting", "wonder"
            ])
        }
        
        return patterns
