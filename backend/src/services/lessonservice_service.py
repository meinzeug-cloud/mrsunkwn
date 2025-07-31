
from typing import List, Optional
from lessonservice_model import LessonServiceCreate, LessonServiceUpdate, LessonServiceInDB, LessonServiceDB
import logging

logger = logging.getLogger(__name__)

class LessonServiceService:
    """Service layer for LessonService operations"""
    
    @staticmethod
    async def create_lessonservice(data: LessonServiceCreate) -> LessonServiceInDB:
        """Create a new lessonservice"""
        try:
            logger.info(f"Creating new lessonservice: {data.name}")
            result = await LessonServiceDB.create(data)
            logger.info(f"LessonService created successfully with ID: {result.id}")
            return result
        except Exception as e:
            logger.error(f"Error creating lessonservice: {str(e)}")
            raise
    
    @staticmethod
    async def get_lessonservice_by_id(id: int) -> Optional[LessonServiceInDB]:
        """Get lessonservice by ID"""
        try:
            logger.info(f"Fetching lessonservice with ID: {id}")
            result = await LessonServiceDB.get_by_id(id)
            if not result:
                logger.warning(f"LessonService with ID {id} not found")
            return result
        except Exception as e:
            logger.error(f"Error fetching lessonservice: {str(e)}")
            raise
    
    @staticmethod
    async def get_all_lessonservices() -> List[LessonServiceInDB]:
        """Get all lessonservices"""
        try:
            logger.info(f"Fetching all lessonservices")
            result = await LessonServiceDB.get_all()
            logger.info(f"Found {len(result)} lessonservices")
            return result
        except Exception as e:
            logger.error(f"Error fetching lessonservices: {str(e)}")
            raise
    
    @staticmethod
    async def update_lessonservice(id: int, data: LessonServiceUpdate) -> Optional[LessonServiceInDB]:
        """Update lessonservice by ID"""
        try:
            logger.info(f"Updating lessonservice with ID: {id}")
            
            # Check if lessonservice exists
            existing = await LessonServiceDB.get_by_id(id)
            if not existing:
                logger.warning(f"LessonService with ID {id} not found for update")
                return None
            
            result = await LessonServiceDB.update(id, data)
            logger.info(f"LessonService updated successfully")
            return result
        except Exception as e:
            logger.error(f"Error updating lessonservice: {str(e)}")
            raise
    
    @staticmethod
    async def delete_lessonservice(id: int) -> bool:
        """Delete lessonservice by ID"""
        try:
            logger.info(f"Deleting lessonservice with ID: {id}")
            
            # Check if lessonservice exists
            existing = await LessonServiceDB.get_by_id(id)
            if not existing:
                logger.warning(f"LessonService with ID {id} not found for deletion")
                return False
            
            result = await LessonServiceDB.delete(id)
            logger.info(f"LessonService deleted successfully")
            return result
        except Exception as e:
            logger.error(f"Error deleting lessonservice: {str(e)}")
            raise
    
    @staticmethod
    async def validate_lessonservice_data(data: LessonServiceCreate) -> bool:
        """Validate lessonservice data before creation"""
        try:
            # Add custom validation logic here
            if not data.name or len(data.name.strip()) == 0:
                logger.warning("Invalid lessonservice data: name is required")
                return False
            
            # Add more validation rules as needed
            logger.info("LessonService data validation passed")
            return True
        except Exception as e:
            logger.error(f"Error validating lessonservice data: {str(e)}")
            return False
