
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class SupportStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"

class SupportBase(BaseModel):
    """Base model for Support"""
    name: str = Field(..., description="Name of the support")
    description: Optional[str] = Field(None, description="Description of the support")
    status: SupportStatus = Field(default=SupportStatus.ACTIVE, description="Status of the support")

class SupportCreate(SupportBase):
    """Model for creating Support"""
    pass

class SupportUpdate(BaseModel):
    """Model for updating Support"""
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[SupportStatus] = None

class SupportInDB(SupportBase):
    """Model for Support in database"""
    id: int = Field(..., description="Unique identifier")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

class SupportResponse(SupportInDB):
    """Model for Support API response"""
    pass

# Database operations (placeholder for actual DB implementation)
class SupportDB:
    @staticmethod
    async def create(data: SupportCreate) -> SupportInDB:
        """Create new support in database"""
        # TODO: Implement database creation
        return SupportInDB(id=1, **data.dict())
    
    @staticmethod
    async def get_by_id(id: int) -> Optional[SupportInDB]:
        """Get support by ID from database"""
        # TODO: Implement database query
        return None
    
    @staticmethod
    async def get_all() -> List[SupportInDB]:
        """Get all supports from database"""
        # TODO: Implement database query
        return []
    
    @staticmethod
    async def update(id: int, data: SupportUpdate) -> Optional[SupportInDB]:
        """Update support in database"""
        # TODO: Implement database update
        return None
    
    @staticmethod
    async def delete(id: int) -> bool:
        """Delete support from database"""
        # TODO: Implement database deletion
        return False
