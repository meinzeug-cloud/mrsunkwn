
from typing import List, Optional
from progressservice_model import ProgressServiceCreate, ProgressServiceUpdate, ProgressServiceInDB, ProgressServiceDB
import logging

logger = logging.getLogger(__name__)

class ProgressServiceService:
    """Service layer for ProgressService operations"""
    
    @staticmethod
    async def create_progressservice(data: ProgressServiceCreate) -> ProgressServiceInDB:
        """Create a new progressservice"""
        try:
            logger.info(f"Creating new progressservice: {data.name}")
            result = await ProgressServiceDB.create(data)
            logger.info(f"ProgressService created successfully with ID: {result.id}")
            return result
        except Exception as e:
            logger.error(f"Error creating progressservice: {str(e)}")
            raise
    
    @staticmethod
    async def get_progressservice_by_id(id: int) -> Optional[ProgressServiceInDB]:
        """Get progressservice by ID"""
        try:
            logger.info(f"Fetching progressservice with ID: {id}")
            result = await ProgressServiceDB.get_by_id(id)
            if not result:
                logger.warning(f"ProgressService with ID {id} not found")
            return result
        except Exception as e:
            logger.error(f"Error fetching progressservice: {str(e)}")
            raise
    
    @staticmethod
    async def get_all_progressservices() -> List[ProgressServiceInDB]:
        """Get all progressservices"""
        try:
            logger.info(f"Fetching all progressservices")
            result = await ProgressServiceDB.get_all()
            logger.info(f"Found {len(result)} progressservices")
            return result
        except Exception as e:
            logger.error(f"Error fetching progressservices: {str(e)}")
            raise
    
    @staticmethod
    async def update_progressservice(id: int, data: ProgressServiceUpdate) -> Optional[ProgressServiceInDB]:
        """Update progressservice by ID"""
        try:
            logger.info(f"Updating progressservice with ID: {id}")
            
            # Check if progressservice exists
            existing = await ProgressServiceDB.get_by_id(id)
            if not existing:
                logger.warning(f"ProgressService with ID {id} not found for update")
                return None
            
            result = await ProgressServiceDB.update(id, data)
            logger.info(f"ProgressService updated successfully")
            return result
        except Exception as e:
            logger.error(f"Error updating progressservice: {str(e)}")
            raise
    
    @staticmethod
    async def delete_progressservice(id: int) -> bool:
        """Delete progressservice by ID"""
        try:
            logger.info(f"Deleting progressservice with ID: {id}")
            
            # Check if progressservice exists
            existing = await ProgressServiceDB.get_by_id(id)
            if not existing:
                logger.warning(f"ProgressService with ID {id} not found for deletion")
                return False
            
            result = await ProgressServiceDB.delete(id)
            logger.info(f"ProgressService deleted successfully")
            return result
        except Exception as e:
            logger.error(f"Error deleting progressservice: {str(e)}")
            raise
    
    @staticmethod
    async def validate_progressservice_data(data: ProgressServiceCreate) -> bool:
        """Validate progressservice data before creation"""
        try:
            # Add custom validation logic here
            if not data.name or len(data.name.strip()) == 0:
                logger.warning("Invalid progressservice data: name is required")
                return False
            
            # Add more validation rules as needed
            logger.info("ProgressService data validation passed")
            return True
        except Exception as e:
            logger.error(f"Error validating progressservice data: {str(e)}")
            return False
