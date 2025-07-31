
from typing import List, Optional
from gradingservice_model import GradingServiceCreate, GradingServiceUpdate, GradingServiceInDB, GradingServiceDB
import logging

logger = logging.getLogger(__name__)

class GradingServiceService:
    """Service layer for GradingService operations"""
    
    @staticmethod
    async def create_gradingservice(data: GradingServiceCreate) -> GradingServiceInDB:
        """Create a new gradingservice"""
        try:
            logger.info(f"Creating new gradingservice: {data.name}")
            result = await GradingServiceDB.create(data)
            logger.info(f"GradingService created successfully with ID: {result.id}")
            return result
        except Exception as e:
            logger.error(f"Error creating gradingservice: {str(e)}")
            raise
    
    @staticmethod
    async def get_gradingservice_by_id(id: int) -> Optional[GradingServiceInDB]:
        """Get gradingservice by ID"""
        try:
            logger.info(f"Fetching gradingservice with ID: {id}")
            result = await GradingServiceDB.get_by_id(id)
            if not result:
                logger.warning(f"GradingService with ID {id} not found")
            return result
        except Exception as e:
            logger.error(f"Error fetching gradingservice: {str(e)}")
            raise
    
    @staticmethod
    async def get_all_gradingservices() -> List[GradingServiceInDB]:
        """Get all gradingservices"""
        try:
            logger.info(f"Fetching all gradingservices")
            result = await GradingServiceDB.get_all()
            logger.info(f"Found {len(result)} gradingservices")
            return result
        except Exception as e:
            logger.error(f"Error fetching gradingservices: {str(e)}")
            raise
    
    @staticmethod
    async def update_gradingservice(id: int, data: GradingServiceUpdate) -> Optional[GradingServiceInDB]:
        """Update gradingservice by ID"""
        try:
            logger.info(f"Updating gradingservice with ID: {id}")
            
            # Check if gradingservice exists
            existing = await GradingServiceDB.get_by_id(id)
            if not existing:
                logger.warning(f"GradingService with ID {id} not found for update")
                return None
            
            result = await GradingServiceDB.update(id, data)
            logger.info(f"GradingService updated successfully")
            return result
        except Exception as e:
            logger.error(f"Error updating gradingservice: {str(e)}")
            raise
    
    @staticmethod
    async def delete_gradingservice(id: int) -> bool:
        """Delete gradingservice by ID"""
        try:
            logger.info(f"Deleting gradingservice with ID: {id}")
            
            # Check if gradingservice exists
            existing = await GradingServiceDB.get_by_id(id)
            if not existing:
                logger.warning(f"GradingService with ID {id} not found for deletion")
                return False
            
            result = await GradingServiceDB.delete(id)
            logger.info(f"GradingService deleted successfully")
            return result
        except Exception as e:
            logger.error(f"Error deleting gradingservice: {str(e)}")
            raise
    
    @staticmethod
    async def validate_gradingservice_data(data: GradingServiceCreate) -> bool:
        """Validate gradingservice data before creation"""
        try:
            # Add custom validation logic here
            if not data.name or len(data.name.strip()) == 0:
                logger.warning("Invalid gradingservice data: name is required")
                return False
            
            # Add more validation rules as needed
            logger.info("GradingService data validation passed")
            return True
        except Exception as e:
            logger.error(f"Error validating gradingservice data: {str(e)}")
            return False
