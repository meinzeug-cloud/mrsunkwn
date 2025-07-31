
from typing import List, Optional
from notificationservice_model import NotificationServiceCreate, NotificationServiceUpdate, NotificationServiceInDB, NotificationServiceDB
import logging

logger = logging.getLogger(__name__)

class NotificationServiceService:
    """Service layer for NotificationService operations"""
    
    @staticmethod
    async def create_notificationservice(data: NotificationServiceCreate) -> NotificationServiceInDB:
        """Create a new notificationservice"""
        try:
            logger.info(f"Creating new notificationservice: {data.name}")
            result = await NotificationServiceDB.create(data)
            logger.info(f"NotificationService created successfully with ID: {result.id}")
            return result
        except Exception as e:
            logger.error(f"Error creating notificationservice: {str(e)}")
            raise
    
    @staticmethod
    async def get_notificationservice_by_id(id: int) -> Optional[NotificationServiceInDB]:
        """Get notificationservice by ID"""
        try:
            logger.info(f"Fetching notificationservice with ID: {id}")
            result = await NotificationServiceDB.get_by_id(id)
            if not result:
                logger.warning(f"NotificationService with ID {id} not found")
            return result
        except Exception as e:
            logger.error(f"Error fetching notificationservice: {str(e)}")
            raise
    
    @staticmethod
    async def get_all_notificationservices() -> List[NotificationServiceInDB]:
        """Get all notificationservices"""
        try:
            logger.info(f"Fetching all notificationservices")
            result = await NotificationServiceDB.get_all()
            logger.info(f"Found {len(result)} notificationservices")
            return result
        except Exception as e:
            logger.error(f"Error fetching notificationservices: {str(e)}")
            raise
    
    @staticmethod
    async def update_notificationservice(id: int, data: NotificationServiceUpdate) -> Optional[NotificationServiceInDB]:
        """Update notificationservice by ID"""
        try:
            logger.info(f"Updating notificationservice with ID: {id}")
            
            # Check if notificationservice exists
            existing = await NotificationServiceDB.get_by_id(id)
            if not existing:
                logger.warning(f"NotificationService with ID {id} not found for update")
                return None
            
            result = await NotificationServiceDB.update(id, data)
            logger.info(f"NotificationService updated successfully")
            return result
        except Exception as e:
            logger.error(f"Error updating notificationservice: {str(e)}")
            raise
    
    @staticmethod
    async def delete_notificationservice(id: int) -> bool:
        """Delete notificationservice by ID"""
        try:
            logger.info(f"Deleting notificationservice with ID: {id}")
            
            # Check if notificationservice exists
            existing = await NotificationServiceDB.get_by_id(id)
            if not existing:
                logger.warning(f"NotificationService with ID {id} not found for deletion")
                return False
            
            result = await NotificationServiceDB.delete(id)
            logger.info(f"NotificationService deleted successfully")
            return result
        except Exception as e:
            logger.error(f"Error deleting notificationservice: {str(e)}")
            raise
    
    @staticmethod
    async def validate_notificationservice_data(data: NotificationServiceCreate) -> bool:
        """Validate notificationservice data before creation"""
        try:
            # Add custom validation logic here
            if not data.name or len(data.name.strip()) == 0:
                logger.warning("Invalid notificationservice data: name is required")
                return False
            
            # Add more validation rules as needed
            logger.info("NotificationService data validation passed")
            return True
        except Exception as e:
            logger.error(f"Error validating notificationservice data: {str(e)}")
            return False
