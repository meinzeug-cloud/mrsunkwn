
from typing import List, Optional
from courseservice_model import CourseServiceCreate, CourseServiceUpdate, CourseServiceInDB, CourseServiceDB
import logging

logger = logging.getLogger(__name__)

class CourseServiceService:
    """Service layer for CourseService operations"""
    
    @staticmethod
    async def create_courseservice(data: CourseServiceCreate) -> CourseServiceInDB:
        """Create a new courseservice"""
        try:
            logger.info(f"Creating new courseservice: {data.name}")
            result = await CourseServiceDB.create(data)
            logger.info(f"CourseService created successfully with ID: {result.id}")
            return result
        except Exception as e:
            logger.error(f"Error creating courseservice: {str(e)}")
            raise
    
    @staticmethod
    async def get_courseservice_by_id(id: int) -> Optional[CourseServiceInDB]:
        """Get courseservice by ID"""
        try:
            logger.info(f"Fetching courseservice with ID: {id}")
            result = await CourseServiceDB.get_by_id(id)
            if not result:
                logger.warning(f"CourseService with ID {id} not found")
            return result
        except Exception as e:
            logger.error(f"Error fetching courseservice: {str(e)}")
            raise
    
    @staticmethod
    async def get_all_courseservices() -> List[CourseServiceInDB]:
        """Get all courseservices"""
        try:
            logger.info(f"Fetching all courseservices")
            result = await CourseServiceDB.get_all()
            logger.info(f"Found {len(result)} courseservices")
            return result
        except Exception as e:
            logger.error(f"Error fetching courseservices: {str(e)}")
            raise
    
    @staticmethod
    async def update_courseservice(id: int, data: CourseServiceUpdate) -> Optional[CourseServiceInDB]:
        """Update courseservice by ID"""
        try:
            logger.info(f"Updating courseservice with ID: {id}")
            
            # Check if courseservice exists
            existing = await CourseServiceDB.get_by_id(id)
            if not existing:
                logger.warning(f"CourseService with ID {id} not found for update")
                return None
            
            result = await CourseServiceDB.update(id, data)
            logger.info(f"CourseService updated successfully")
            return result
        except Exception as e:
            logger.error(f"Error updating courseservice: {str(e)}")
            raise
    
    @staticmethod
    async def delete_courseservice(id: int) -> bool:
        """Delete courseservice by ID"""
        try:
            logger.info(f"Deleting courseservice with ID: {id}")
            
            # Check if courseservice exists
            existing = await CourseServiceDB.get_by_id(id)
            if not existing:
                logger.warning(f"CourseService with ID {id} not found for deletion")
                return False
            
            result = await CourseServiceDB.delete(id)
            logger.info(f"CourseService deleted successfully")
            return result
        except Exception as e:
            logger.error(f"Error deleting courseservice: {str(e)}")
            raise
    
    @staticmethod
    async def validate_courseservice_data(data: CourseServiceCreate) -> bool:
        """Validate courseservice data before creation"""
        try:
            # Add custom validation logic here
            if not data.name or len(data.name.strip()) == 0:
                logger.warning("Invalid courseservice data: name is required")
                return False
            
            # Add more validation rules as needed
            logger.info("CourseService data validation passed")
            return True
        except Exception as e:
            logger.error(f"Error validating courseservice data: {str(e)}")
            return False
