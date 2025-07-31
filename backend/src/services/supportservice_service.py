
from typing import List, Optional
from supportservice_model import SupportServiceCreate, SupportServiceUpdate, SupportServiceInDB, SupportServiceDB
import logging

logger = logging.getLogger(__name__)

class SupportServiceService:
    """Service layer for SupportService operations"""
    
    @staticmethod
    async def create_supportservice(data: SupportServiceCreate) -> SupportServiceInDB:
        """Create a new supportservice"""
        try:
            logger.info(f"Creating new supportservice: {data.name}")
            result = await SupportServiceDB.create(data)
            logger.info(f"SupportService created successfully with ID: {result.id}")
            return result
        except Exception as e:
            logger.error(f"Error creating supportservice: {str(e)}")
            raise
    
    @staticmethod
    async def get_supportservice_by_id(id: int) -> Optional[SupportServiceInDB]:
        """Get supportservice by ID"""
        try:
            logger.info(f"Fetching supportservice with ID: {id}")
            result = await SupportServiceDB.get_by_id(id)
            if not result:
                logger.warning(f"SupportService with ID {id} not found")
            return result
        except Exception as e:
            logger.error(f"Error fetching supportservice: {str(e)}")
            raise
    
    @staticmethod
    async def get_all_supportservices() -> List[SupportServiceInDB]:
        """Get all supportservices"""
        try:
            logger.info(f"Fetching all supportservices")
            result = await SupportServiceDB.get_all()
            logger.info(f"Found {len(result)} supportservices")
            return result
        except Exception as e:
            logger.error(f"Error fetching supportservices: {str(e)}")
            raise
    
    @staticmethod
    async def update_supportservice(id: int, data: SupportServiceUpdate) -> Optional[SupportServiceInDB]:
        """Update supportservice by ID"""
        try:
            logger.info(f"Updating supportservice with ID: {id}")
            
            # Check if supportservice exists
            existing = await SupportServiceDB.get_by_id(id)
            if not existing:
                logger.warning(f"SupportService with ID {id} not found for update")
                return None
            
            result = await SupportServiceDB.update(id, data)
            logger.info(f"SupportService updated successfully")
            return result
        except Exception as e:
            logger.error(f"Error updating supportservice: {str(e)}")
            raise
    
    @staticmethod
    async def delete_supportservice(id: int) -> bool:
        """Delete supportservice by ID"""
        try:
            logger.info(f"Deleting supportservice with ID: {id}")
            
            # Check if supportservice exists
            existing = await SupportServiceDB.get_by_id(id)
            if not existing:
                logger.warning(f"SupportService with ID {id} not found for deletion")
                return False
            
            result = await SupportServiceDB.delete(id)
            logger.info(f"SupportService deleted successfully")
            return result
        except Exception as e:
            logger.error(f"Error deleting supportservice: {str(e)}")
            raise
    
    @staticmethod
    async def validate_supportservice_data(data: SupportServiceCreate) -> bool:
        """Validate supportservice data before creation"""
        try:
            # Add custom validation logic here
            if not data.name or len(data.name.strip()) == 0:
                logger.warning("Invalid supportservice data: name is required")
                return False
            
            # Add more validation rules as needed
            logger.info("SupportService data validation passed")
            return True
        except Exception as e:
            logger.error(f"Error validating supportservice data: {str(e)}")
            return False
