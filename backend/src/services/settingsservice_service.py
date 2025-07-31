
from typing import List, Optional
from settingsservice_model import SettingsServiceCreate, SettingsServiceUpdate, SettingsServiceInDB, SettingsServiceDB
import logging

logger = logging.getLogger(__name__)

class SettingsServiceService:
    """Service layer for SettingsService operations"""
    
    @staticmethod
    async def create_settingsservice(data: SettingsServiceCreate) -> SettingsServiceInDB:
        """Create a new settingsservice"""
        try:
            logger.info(f"Creating new settingsservice: {data.name}")
            result = await SettingsServiceDB.create(data)
            logger.info(f"SettingsService created successfully with ID: {result.id}")
            return result
        except Exception as e:
            logger.error(f"Error creating settingsservice: {str(e)}")
            raise
    
    @staticmethod
    async def get_settingsservice_by_id(id: int) -> Optional[SettingsServiceInDB]:
        """Get settingsservice by ID"""
        try:
            logger.info(f"Fetching settingsservice with ID: {id}")
            result = await SettingsServiceDB.get_by_id(id)
            if not result:
                logger.warning(f"SettingsService with ID {id} not found")
            return result
        except Exception as e:
            logger.error(f"Error fetching settingsservice: {str(e)}")
            raise
    
    @staticmethod
    async def get_all_settingsservices() -> List[SettingsServiceInDB]:
        """Get all settingsservices"""
        try:
            logger.info(f"Fetching all settingsservices")
            result = await SettingsServiceDB.get_all()
            logger.info(f"Found {len(result)} settingsservices")
            return result
        except Exception as e:
            logger.error(f"Error fetching settingsservices: {str(e)}")
            raise
    
    @staticmethod
    async def update_settingsservice(id: int, data: SettingsServiceUpdate) -> Optional[SettingsServiceInDB]:
        """Update settingsservice by ID"""
        try:
            logger.info(f"Updating settingsservice with ID: {id}")
            
            # Check if settingsservice exists
            existing = await SettingsServiceDB.get_by_id(id)
            if not existing:
                logger.warning(f"SettingsService with ID {id} not found for update")
                return None
            
            result = await SettingsServiceDB.update(id, data)
            logger.info(f"SettingsService updated successfully")
            return result
        except Exception as e:
            logger.error(f"Error updating settingsservice: {str(e)}")
            raise
    
    @staticmethod
    async def delete_settingsservice(id: int) -> bool:
        """Delete settingsservice by ID"""
        try:
            logger.info(f"Deleting settingsservice with ID: {id}")
            
            # Check if settingsservice exists
            existing = await SettingsServiceDB.get_by_id(id)
            if not existing:
                logger.warning(f"SettingsService with ID {id} not found for deletion")
                return False
            
            result = await SettingsServiceDB.delete(id)
            logger.info(f"SettingsService deleted successfully")
            return result
        except Exception as e:
            logger.error(f"Error deleting settingsservice: {str(e)}")
            raise
    
    @staticmethod
    async def validate_settingsservice_data(data: SettingsServiceCreate) -> bool:
        """Validate settingsservice data before creation"""
        try:
            # Add custom validation logic here
            if not data.name or len(data.name.strip()) == 0:
                logger.warning("Invalid settingsservice data: name is required")
                return False
            
            # Add more validation rules as needed
            logger.info("SettingsService data validation passed")
            return True
        except Exception as e:
            logger.error(f"Error validating settingsservice data: {str(e)}")
            return False
