
from typing import List, Optional
from communicationservice_model import CommunicationServiceCreate, CommunicationServiceUpdate, CommunicationServiceInDB, CommunicationServiceDB
import logging

logger = logging.getLogger(__name__)

class CommunicationServiceService:
    """Service layer for CommunicationService operations"""
    
    @staticmethod
    async def create_communicationservice(data: CommunicationServiceCreate) -> CommunicationServiceInDB:
        """Create a new communicationservice"""
        try:
            logger.info(f"Creating new communicationservice: {data.name}")
            result = await CommunicationServiceDB.create(data)
            logger.info(f"CommunicationService created successfully with ID: {result.id}")
            return result
        except Exception as e:
            logger.error(f"Error creating communicationservice: {str(e)}")
            raise
    
    @staticmethod
    async def get_communicationservice_by_id(id: int) -> Optional[CommunicationServiceInDB]:
        """Get communicationservice by ID"""
        try:
            logger.info(f"Fetching communicationservice with ID: {id}")
            result = await CommunicationServiceDB.get_by_id(id)
            if not result:
                logger.warning(f"CommunicationService with ID {id} not found")
            return result
        except Exception as e:
            logger.error(f"Error fetching communicationservice: {str(e)}")
            raise
    
    @staticmethod
    async def get_all_communicationservices() -> List[CommunicationServiceInDB]:
        """Get all communicationservices"""
        try:
            logger.info(f"Fetching all communicationservices")
            result = await CommunicationServiceDB.get_all()
            logger.info(f"Found {len(result)} communicationservices")
            return result
        except Exception as e:
            logger.error(f"Error fetching communicationservices: {str(e)}")
            raise
    
    @staticmethod
    async def update_communicationservice(id: int, data: CommunicationServiceUpdate) -> Optional[CommunicationServiceInDB]:
        """Update communicationservice by ID"""
        try:
            logger.info(f"Updating communicationservice with ID: {id}")
            
            # Check if communicationservice exists
            existing = await CommunicationServiceDB.get_by_id(id)
            if not existing:
                logger.warning(f"CommunicationService with ID {id} not found for update")
                return None
            
            result = await CommunicationServiceDB.update(id, data)
            logger.info(f"CommunicationService updated successfully")
            return result
        except Exception as e:
            logger.error(f"Error updating communicationservice: {str(e)}")
            raise
    
    @staticmethod
    async def delete_communicationservice(id: int) -> bool:
        """Delete communicationservice by ID"""
        try:
            logger.info(f"Deleting communicationservice with ID: {id}")
            
            # Check if communicationservice exists
            existing = await CommunicationServiceDB.get_by_id(id)
            if not existing:
                logger.warning(f"CommunicationService with ID {id} not found for deletion")
                return False
            
            result = await CommunicationServiceDB.delete(id)
            logger.info(f"CommunicationService deleted successfully")
            return result
        except Exception as e:
            logger.error(f"Error deleting communicationservice: {str(e)}")
            raise
    
    @staticmethod
    async def validate_communicationservice_data(data: CommunicationServiceCreate) -> bool:
        """Validate communicationservice data before creation"""
        try:
            # Add custom validation logic here
            if not data.name or len(data.name.strip()) == 0:
                logger.warning("Invalid communicationservice data: name is required")
                return False
            
            # Add more validation rules as needed
            logger.info("CommunicationService data validation passed")
            return True
        except Exception as e:
            logger.error(f"Error validating communicationservice data: {str(e)}")
            return False
