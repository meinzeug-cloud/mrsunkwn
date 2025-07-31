
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class CourseStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"

class CourseBase(BaseModel):
    """Base model for Course"""
    name: str = Field(..., description="Name of the course")
    description: Optional[str] = Field(None, description="Description of the course")
    status: CourseStatus = Field(default=CourseStatus.ACTIVE, description="Status of the course")

class CourseCreate(CourseBase):
    """Model for creating Course"""
    pass

class CourseUpdate(BaseModel):
    """Model for updating Course"""
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[CourseStatus] = None

class CourseInDB(CourseBase):
    """Model for Course in database"""
    id: int = Field(..., description="Unique identifier")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

class CourseResponse(CourseInDB):
    """Model for Course API response"""
    pass

# Database operations (placeholder for actual DB implementation)
class CourseDB:
    @staticmethod
    async def create(data: CourseCreate) -> CourseInDB:
        """Create new course in database"""
        # TODO: Implement database creation
        return CourseInDB(id=1, **data.dict())
    
    @staticmethod
    async def get_by_id(id: int) -> Optional[CourseInDB]:
        """Get course by ID from database"""
        # TODO: Implement database query
        return None
    
    @staticmethod
    async def get_all() -> List[CourseInDB]:
        """Get all courses from database"""
        # TODO: Implement database query
        return []
    
    @staticmethod
    async def update(id: int, data: CourseUpdate) -> Optional[CourseInDB]:
        """Update course in database"""
        # TODO: Implement database update
        return None
    
    @staticmethod
    async def delete(id: int) -> bool:
        """Delete course from database"""
        # TODO: Implement database deletion
        return False
