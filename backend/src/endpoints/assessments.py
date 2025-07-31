
from fastapi import APIRouter, HTTPException, Depends, Query, Path, status, BackgroundTasks
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, validator
from datetime import datetime, timedelta
from enum import Enum
import logging
import asyncio
import json
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user, get_current_parent, verify_permissions
from models.assessments import Assessments
from services.assessments_service import AssessmentsService
from services.ai_tutor_service import AITutorService
from services.anti_cheat_service import AntiCheatService
from monitoring.activity_logger import log_user_activity

# Setup logging
logger = logging.getLogger(__name__)

# Create router with Mrs-Unkwn specific configuration
router = APIRouter(
    prefix="/api/assessments",
    tags=["assessments"],
    responses={
        404: {"description": "Resource not found"},
        403: {"description": "Access forbidden - Parental controls or permissions"},
        422: {"description": "Validation error"},
        429: {"description": "Rate limit exceeded"},
        500: {"description": "Internal server error"}
    }
)

# Mrs-Unkwn specific enums and models
class MrsUnkwnStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    LEARNING = "learning"
    BLOCKED = "blocked"
    SUSPENDED = "suspended"
    MONITORED = "monitored"

class LearningMode(str, Enum):
    SOCRATIC = "socratic"
    GUIDED = "guided"
    PRACTICE = "practice"
    ASSESSMENT = "assessment"
    FREE_EXPLORATION = "free_exploration"

class ParentalControlLevel(str, Enum):
    MINIMAL = "minimal"
    STANDARD = "standard"
    STRICT = "strict"
    CUSTOM = "custom"

# Enhanced base models for Mrs-Unkwn
class AssessmentsBase(BaseModel):
    """Base model for assessments with Mrs-Unkwn specific fields"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    status: MrsUnkwnStatus = Field(default=MrsUnkwnStatus.ACTIVE)
    learning_mode: Optional[LearningMode] = Field(None)
    parental_control_level: ParentalControlLevel = Field(default=ParentalControlLevel.STANDARD)
    subject_areas: List[str] = Field(default_factory=list)
    difficulty_level: int = Field(default=5, ge=1, le=10)
    age_appropriate: bool = Field(default=True)
    requires_parent_approval: bool = Field(default=False)
    ai_interaction_enabled: bool = Field(default=True)
    monitoring_level: str = Field(default="standard")
    gamification_enabled: bool = Field(default=True)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    @validator('subject_areas')
    def validate_subjects(cls, v):
        valid_subjects = [
            'mathematics', 'science', 'english', 'history', 
            'geography', 'art', 'music', 'programming', 'languages'
        ]
        for subject in v:
            if subject.lower() not in valid_subjects:
                raise ValueError(f'Invalid subject: {subject}')
        return v

class AssessmentsCreate(AssessmentsBase):
    """Model for creating assessments with Mrs-Unkwn features"""
    student_id: Optional[str] = Field(None, description="Associated student ID")
    parent_id: Optional[str] = Field(None, description="Associated parent ID")
    family_id: str = Field(..., description="Family ID for access control")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Mathematics Learning Session",
                "description": "Algebra practice with AI tutor guidance",
                "status": "active",
                "learning_mode": "socratic",
                "parental_control_level": "standard",
                "subject_areas": ["mathematics"],
                "difficulty_level": 6,
                "student_id": "student_123",
                "family_id": "family_456"
            }
        }

class AssessmentsResponse(AssessmentsBase):
    """Response model with Mrs-Unkwn analytics"""
    id: str = Field(..., description="Unique identifier")
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: str
    family_id: str
    
    # Mrs-Unkwn specific analytics
    total_learning_time: timedelta = Field(default=timedelta(0))
    ai_interactions_count: int = Field(default=0)
    achievements_earned: List[str] = Field(default_factory=list)
    current_streak: int = Field(default=0)
    safety_violations: int = Field(default=0)
    parent_interventions: int = Field(default=0)
    learning_progress_score: float = Field(default=0.0, ge=0.0, le=1.0)
    
    class Config:
        schema_extra = {
            "example": {
                "id": "session_789",
                "name": "Mathematics Learning Session",
                "status": "learning",
                "total_learning_time": "PT2H30M",
                "ai_interactions_count": 45,
                "achievements_earned": ["first_equation", "streak_7_days"],
                "current_streak": 7,
                "learning_progress_score": 0.78
            }
        }

# Mrs-Unkwn specific dependency functions
async def verify_family_access(
    item_id: str, 
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Verify user has family access to resource"""
    # TODO: Implement family access verification
    return True

async def check_parental_controls(
    student_id: str,
    action: str,
    db: Session = Depends(get_db)
):
    """Check if action is allowed by parental controls"""
    # TODO: Implement parental control checks
    return True

async def log_learning_activity(
    user_id: str,
    activity_type: str,
    details: Dict[str, Any],
    background_tasks: BackgroundTasks
):
    """Log learning activity for analytics"""
    background_tasks.add_task(
        log_user_activity,
        user_id=user_id,
        activity_type=activity_type,
        details=details
    )

# Main CRUD endpoints with Mrs-Unkwn features
@router.get(
    "/",
    response_model=List[AssessmentsResponse],
    summary="Get assessmentss for family",
    description="Retrieve family's assessmentss with parental filtering"
)
async def get_assessmentss(
    family_id: Optional[str] = Query(None, description="Filter by family ID"),
    student_id: Optional[str] = Query(None, description="Filter by student ID"),
    subject: Optional[str] = Query(None, description="Filter by subject area"),
    status: Optional[MrsUnkwnStatus] = Query(None, description="Filter by status"),
    learning_mode: Optional[LearningMode] = Query(None, description="Filter by learning mode"),
    date_from: Optional[datetime] = Query(None, description="Filter from date"),
    date_to: Optional[datetime] = Query(None, description="Filter to date"),
    include_analytics: bool = Query(True, description="Include learning analytics"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """Get assessmentss with Mrs-Unkwn family filtering and analytics"""
    try:
        # Log access attempt
        await log_learning_activity(
            current_user.id, 
            "view_assessmentss", 
            {"family_id": family_id, "filters": {"subject": subject, "status": status}},
            background_tasks
        )
        
        # Verify family access
        if family_id and not await verify_family_access(family_id, current_user, db):
            raise HTTPException(status_code=403, detail="Access to family data forbidden")
        
        # Build comprehensive filters
        filters = {
            "family_id": family_id or current_user.family_id,
            "student_id": student_id,
            "subject": subject,
            "status": status,
            "learning_mode": learning_mode,
            "date_from": date_from,
            "date_to": date_to
        }
        
        # Get data through service layer
        service = AssessmentsService(db)
        items = await service.get_filtered_assessmentss(
            filters=filters,
            include_analytics=include_analytics,
            page=page,
            per_page=per_page
        )
        
        logger.info(f"Retrieved {len(items)} assessmentss for user {current_user.id}")
        return items
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving assessmentss: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving data")

@router.post(
    "/",
    response_model=AssessmentsResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new assessments",
    description="Create new assessments with AI tutor integration"
)
async def create_assessments(
    request: AssessmentsCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """Create new assessments with Mrs-Unkwn features"""
    try:
        # Check parental controls if this is for a student
        if request.student_id:
            allowed = await check_parental_controls(
                request.student_id, 
                "create_assessments",
                db
            )
            if not allowed:
                raise HTTPException(
                    status_code=403, 
                    detail="Action blocked by parental controls"
                )
        
        # Verify family membership
        if not await verify_family_access(request.family_id, current_user, db):
            raise HTTPException(status_code=403, detail="Family access required")
        
        # Create through service layer
        service = AssessmentsService(db)
        new_item = await service.create_assessments(request, current_user.id)
        
        # Initialize AI tutor if enabled
        if request.ai_interaction_enabled:
            ai_service = AITutorService()
            await ai_service.initialize_for_assessments(new_item.id)
        
        # Log creation activity
        await log_learning_activity(
            current_user.id,
            "create_assessments",
            {"item_id": new_item.id, "name": request.name},
            background_tasks
        )
        
        logger.info(f"Created assessments {new_item.id} for user {current_user.id}")
        return new_item
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating assessments: {str(e)}")
        raise HTTPException(status_code=500, detail="Error creating resource")

@router.get(
    "/{item_id}",
    response_model=AssessmentsResponse,
    summary="Get assessments by ID",
    description="Get specific assessments with real-time monitoring data"
)
async def get_assessments(
    item_id: str = Path(..., description="ID of the assessments"),
    include_live_data: bool = Query(True, description="Include real-time monitoring data"),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """Get assessments with Mrs-Unkwn monitoring integration"""
    try:
        # Verify access
        if not await verify_family_access(item_id, current_user, db):
            raise HTTPException(status_code=403, detail="Access forbidden")
        
        # Get through service
        service = AssessmentsService(db)
        item = await service.get_assessments_by_id(item_id, include_live_data)
        
        if not item:
            raise HTTPException(status_code=404, detail="Assessments not found")
        
        # Check for any active anti-cheat alerts
        if include_live_data:
            anti_cheat_service = AntiCheatService()
            alerts = await anti_cheat_service.get_active_alerts(item_id)
            if alerts:
                item.metadata["active_alerts"] = len(alerts)
        
        # Log access
        await log_learning_activity(
            current_user.id,
            "view_assessments",
            {"item_id": item_id},
            background_tasks
        )
        
        return item
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving assessments {item_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving resource")

# Mrs-Unkwn specific endpoints
@router.post(
    "/{item_id}/ai-interaction",
    summary="AI Tutor Interaction",
    description="Interact with AI tutor for this assessments"
)
async def ai_tutor_interaction(
    item_id: str = Path(...),
    message: str = Field(..., min_length=1, max_length=2000),
    interaction_type: str = Field(default="question"),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """Handle AI tutor interaction with anti-cheat monitoring"""
    try:
        # Verify access
        if not await verify_family_access(item_id, current_user, db):
            raise HTTPException(status_code=403, detail="Access forbidden")
        
        # Check for cheating patterns
        anti_cheat_service = AntiCheatService()
        is_suspicious = await anti_cheat_service.analyze_interaction(
            user_id=current_user.id,
            message=message,
            context={"item_id": item_id, "type": interaction_type}
        )
        
        if is_suspicious:
            # Log suspicious activity and notify parents
            await anti_cheat_service.handle_suspicious_activity(
                current_user.id, 
                "suspicious_ai_interaction", 
                {"message": message[:100]}
            )
            
        # Process through AI tutor with Socratic method
        ai_service = AITutorService()
        response = await ai_service.process_socratic_interaction(
            item_id=item_id,
            user_message=message,
            user_id=current_user.id,
            apply_pedagogy=True
        )
        
        # Log interaction
        await log_learning_activity(
            current_user.id,
            "ai_interaction",
            {
                "item_id": item_id,
                "interaction_type": interaction_type,
                "message_length": len(message),
                "response_type": response.get("type", "unknown")
            },
            background_tasks
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in AI interaction: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing AI interaction")

@router.get(
    "/{item_id}/learning-analytics",
    summary="Get Learning Analytics",
    description="Get comprehensive learning analytics for this assessments"
)
async def get_learning_analytics(
    item_id: str = Path(...),
    time_range: str = Query("week", regex="^(day|week|month|year)$"),
    include_ai_insights: bool = Query(True),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get Mrs-Unkwn learning analytics with AI insights"""
    try:
        # Verify access
        if not await verify_family_access(item_id, current_user, db):
            raise HTTPException(status_code=403, detail="Access forbidden")
        
        # Get analytics through service
        analytics_service = LearningAnalyticsService(db)
        analytics = await analytics_service.get_comprehensive_analytics(
            item_id=item_id,
            time_range=time_range,
            include_ai_insights=include_ai_insights
        )
        
        return analytics
        
    except Exception as e:
        logger.error(f"Error getting analytics: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving analytics")

@router.post(
    "/{item_id}/parent-intervention",
    summary="Parent Intervention",
    description="Parent intervention actions for learning session"
)
async def parent_intervention(
    item_id: str = Path(...),
    action: str = Field(..., regex="^(pause|resume|block|allow|redirect)$"),
    message: Optional[str] = Field(None, max_length=500),
    current_user = Depends(get_current_parent),
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """Handle parent intervention in learning session"""
    try:
        # Verify parent access
        if not await verify_family_access(item_id, current_user, db):
            raise HTTPException(status_code=403, detail="Parent access required")
        
        # Execute intervention through service
        service = AssessmentsService(db)
        result = await service.execute_parent_intervention(
            item_id=item_id,
            action=action,
            message=message,
            parent_id=current_user.id
        )
        
        # Log intervention
        await log_learning_activity(
            current_user.id,
            "parent_intervention",
            {
                "item_id": item_id,
                "action": action,
                "has_message": bool(message)
            },
            background_tasks
        )
        
        return {"success": True, "action": action, "result": result}
        
    except Exception as e:
        logger.error(f"Error in parent intervention: {str(e)}")
        raise HTTPException(status_code=500, detail="Error executing intervention")
