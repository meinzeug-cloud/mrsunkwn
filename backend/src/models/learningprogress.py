
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class MrsUnkwnStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive" 
    LEARNING = "learning"
    BLOCKED = "blocked"
    SUSPENDED = "suspended"

class LearningProgressPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

# SQLAlchemy Model (Database)
class LearningProgressDB(Base):
    """SQLAlchemy model for LearningProgress in database"""
    __tablename__ = "learningprogresss"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(String(20), default=MrsUnkwnStatus.ACTIVE.value, index=True)
    priority = Column(String(20), default=LearningProgressPriority.MEDIUM.value)
    
    # Mrs-Unkwn specific fields
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    family_id = Column(String, ForeignKey("families.id"), nullable=False, index=True)
    subject_areas = Column(JSON, default=list)
    difficulty_level = Column(Integer, default=5)
    age_appropriate = Column(Boolean, default=True)
    requires_parent_approval = Column(Boolean, default=False)
    ai_interaction_enabled = Column(Boolean, default=True)
    monitoring_level = Column(String(20), default="standard")
    gamification_enabled = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Analytics fields
    total_learning_time = Column(Integer, default=0)  # seconds
    ai_interactions_count = Column(Integer, default=0)
    achievements_earned = Column(JSON, default=list)
    current_streak = Column(Integer, default=0)
    safety_violations = Column(Integer, default=0)
    parent_interventions = Column(Integer, default=0)
    learning_progress_score = Column(Float, default=0.0)
    
    # Metadata
    metadata = Column(JSON, default=dict)
    version = Column(Integer, default=1)
    
    # Relationships
    user = relationship("User", back_populates="learningprogresss")
    family = relationship("Family", back_populates="learningprogresss")

# Pydantic Models (API)
class LearningProgressBase(BaseModel):
    """Base model for LearningProgress API operations"""
    name: str = Field(..., min_length=1, max_length=255, description="Name of the learningprogress")
    description: Optional[str] = Field(None, max_length=1000, description="Description")
    status: MrsUnkwnStatus = Field(default=MrsUnkwnStatus.ACTIVE)
    priority: LearningProgressPriority = Field(default=LearningProgressPriority.MEDIUM)
    subject_areas: List[str] = Field(default_factory=list, description="Subject areas")
    difficulty_level: int = Field(default=5, ge=1, le=10, description="Difficulty level (1-10)")
    age_appropriate: bool = Field(default=True, description="Age appropriate content")
    requires_parent_approval: bool = Field(default=False, description="Requires parent approval")
    ai_interaction_enabled: bool = Field(default=True, description="AI interaction enabled")
    monitoring_level: str = Field(default="standard", description="Monitoring level")
    gamification_enabled: bool = Field(default=True, description="Gamification enabled")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
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
    
    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty or only whitespace')
        return v.strip()

class LearningProgressCreate(LearningProgressBase):
    """Model for creating new LearningProgress"""
    user_id: str = Field(..., description="User ID who owns this learningprogress")
    family_id: str = Field(..., description="Family ID for access control")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Sample LearningProgress",
                "description": "A sample learningprogress for demonstration",
                "status": "active",
                "priority": "medium",
                "subject_areas": ["mathematics", "science"],
                "difficulty_level": 6,
                "user_id": "user_123",
                "family_id": "family_456",
                "age_appropriate": True,
                "ai_interaction_enabled": True
            }
        }

class LearningProgressUpdate(BaseModel):
    """Model for updating LearningProgress"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[MrsUnkwnStatus] = None
    priority: Optional[LearningProgressPriority] = None
    subject_areas: Optional[List[str]] = None
    difficulty_level: Optional[int] = Field(None, ge=1, le=10)
    age_appropriate: Optional[bool] = None
    requires_parent_approval: Optional[bool] = None
    ai_interaction_enabled: Optional[bool] = None
    monitoring_level: Optional[str] = None
    gamification_enabled: Optional[bool] = None
    metadata: Optional[Dict[str, Any]] = None
    
    @validator('name')
    def validate_name(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Name cannot be empty or only whitespace')
        return v.strip() if v else v

class LearningProgressInDB(LearningProgressBase):
    """Model for LearningProgress as stored in database"""
    id: str = Field(..., description="Unique identifier")
    user_id: str = Field(..., description="Owner user ID")
    family_id: str = Field(..., description="Family ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    
    # Analytics data
    total_learning_time: timedelta = Field(default=timedelta(0), description="Total learning time")
    ai_interactions_count: int = Field(default=0, description="Number of AI interactions")
    achievements_earned: List[str] = Field(default_factory=list, description="Earned achievements")
    current_streak: int = Field(default=0, description="Current learning streak")
    safety_violations: int = Field(default=0, description="Safety violations count")
    parent_interventions: int = Field(default=0, description="Parent interventions count")
    learning_progress_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Learning progress score")
    version: int = Field(default=1, description="Version for optimistic locking")
    
    class Config:
        orm_mode = True

class LearningProgressResponse(LearningProgressInDB):
    """Model for LearningProgress API response"""
    
    class Config:
        schema_extra = {
            "example": {
                "id": "learningprogress_123",
                "name": "Sample LearningProgress",
                "description": "A sample learningprogress",
                "status": "active",
                "priority": "medium",
                "user_id": "user_123",
                "family_id": "family_456",
                "subject_areas": ["mathematics"],
                "difficulty_level": 6,
                "created_at": "2023-01-01T00:00:00Z",
                "total_learning_time": "PT2H30M",
                "ai_interactions_count": 45,
                "current_streak": 7,
                "learning_progress_score": 0.78
            }
        }

class LearningProgressList(BaseModel):
    """Model for paginated LearningProgress list response"""
    items: List[LearningProgressResponse] = Field(..., description="List of learningprogresss")
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    per_page: int = Field(..., description="Items per page")
    pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Has next page")
    has_prev: bool = Field(..., description="Has previous page")

class LearningProgressAnalytics(BaseModel):
    """Model for LearningProgress analytics data"""
    user_id: str
    family_id: str
    timeframe: str
    total_items: int
    active_items: int
    completed_items: int
    average_difficulty: float
    total_learning_time: timedelta
    ai_interactions: int
    achievements_count: int
    progress_trend: str
    recommendations: List[str]
    generated_at: datetime

# Database operations class
class LearningProgressOperations:
    """Database operations for LearningProgress"""
    
    def __init__(self, db):
        self.db = db
    
    async def create(self, data: LearningProgressCreate) -> LearningProgressInDB:
        """Create new learningprogress in database"""
        import uuid
        
        db_item = LearningProgressDB(
            id=str(uuid.uuid4()),
            **data.dict(),
            created_at=datetime.utcnow()
        )
        
        self.db.add(db_item)
        await self.db.commit()
        await self.db.refresh(db_item)
        
        return LearningProgressInDB.from_orm(db_item)
    
    async def get_by_id(self, item_id: str) -> Optional[LearningProgressInDB]:
        """Get learningprogress by ID"""
        db_item = await self.db.query(LearningProgressDB).filter(
            LearningProgressDB.id == item_id
        ).first()
        
        return LearningProgressInDB.from_orm(db_item) if db_item else None
    
    async def get_by_user(self, user_id: str, page: int = 1, per_page: int = 20) -> LearningProgressList:
        """Get learningprogresss by user ID"""
        offset = (page - 1) * per_page
        
        query = self.db.query(LearningProgressDB).filter(
            LearningProgressDB.user_id == user_id
        )
        
        total = await query.count()
        items = await query.offset(offset).limit(per_page).all()
        
        return LearningProgressList(
            items=[LearningProgressResponse.from_orm(item) for item in items],
            total=total,
            page=page,
            per_page=per_page,
            pages=(total + per_page - 1) // per_page,
            has_next=page * per_page < total,
            has_prev=page > 1
        )
    
    async def update(self, item_id: str, data: LearningProgressUpdate) -> Optional[LearningProgressInDB]:
        """Update learningprogress by ID"""
        db_item = await self.db.query(LearningProgressDB).filter(
            LearningProgressDB.id == item_id
        ).first()
        
        if not db_item:
            return None
        
        update_data = data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_item, field, value)
        
        db_item.updated_at = datetime.utcnow()
        db_item.version += 1
        
        await self.db.commit()
        await self.db.refresh(db_item)
        
        return LearningProgressInDB.from_orm(db_item)
    
    async def delete(self, item_id: str) -> bool:
        """Delete learningprogress by ID"""
        db_item = await self.db.query(LearningProgressDB).filter(
            LearningProgressDB.id == item_id
        ).first()
        
        if not db_item:
            return False
        
        await self.db.delete(db_item)
        await self.db.commit()
        
        return True
    
    async def get_analytics(self, user_id: str, timeframe: str = "week") -> LearningProgressAnalytics:
        """Get analytics for learningprogresss"""
        # Implementation would include complex analytics queries
        return LearningProgressAnalytics(
            user_id=user_id,
            family_id="family_123",
            timeframe=timeframe,
            total_items=10,
            active_items=8,
            completed_items=2,
            average_difficulty=6.5,
            total_learning_time=timedelta(hours=25),
            ai_interactions=150,
            achievements_count=12,
            progress_trend="improving",
            recommendations=["Continue current pace", "Try harder challenges"],
            generated_at=datetime.utcnow()
        )
