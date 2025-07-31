
from typing import List, Optional
from tutorservice_model import TutorServiceCreate, TutorServiceUpdate, TutorServiceInDB, TutorServiceDB
import logging

logger = logging.getLogger(__name__)

class TutorServiceService:
    """Service layer for TutorService operations"""
    
    @staticmethod
    async def create_tutorservice(data: TutorServiceCreate) -> TutorServiceInDB:
        """Create a new tutorservice"""
        try:
            logger.info(f"Creating new tutorservice: {data.name}")
            result = await TutorServiceDB.create(data)
            logger.info(f"TutorService created successfully with ID: {result.id}")
            return result
        except Exception as e:
            logger.error(f"Error creating tutorservice: {str(e)}")
            raise
    
    @staticmethod
    async def get_tutorservice_by_id(id: int) -> Optional[TutorServiceInDB]:
        """Get tutorservice by ID"""
        try:
            logger.info(f"Fetching tutorservice with ID: {id}")
            result = await TutorServiceDB.get_by_id(id)
            if not result:
                logger.warning(f"TutorService with ID {id} not found")
            return result
        except Exception as e:
            logger.error(f"Error fetching tutorservice: {str(e)}")
            raise
    
    @staticmethod
    async def get_all_tutorservices() -> List[TutorServiceInDB]:
        """Get all tutorservices"""
        try:
            logger.info(f"Fetching all tutorservices")
            result = await TutorServiceDB.get_all()
            logger.info(f"Found {len(result)} tutorservices")
            return result
        except Exception as e:
            logger.error(f"Error fetching tutorservices: {str(e)}")
            raise
    
    @staticmethod
    async def update_tutorservice(id: int, data: TutorServiceUpdate) -> Optional[TutorServiceInDB]:
        """Update tutorservice by ID"""
        try:
            logger.info(f"Updating tutorservice with ID: {id}")
            
            # Check if tutorservice exists
            existing = await TutorServiceDB.get_by_id(id)
            if not existing:
                logger.warning(f"TutorService with ID {id} not found for update")
                return None
            
            result = await TutorServiceDB.update(id, data)
            logger.info(f"TutorService updated successfully")
            return result
        except Exception as e:
            logger.error(f"Error updating tutorservice: {str(e)}")
            raise
    
    @staticmethod
    async def delete_tutorservice(id: int) -> bool:
        """Delete tutorservice by ID"""
        try:
            logger.info(f"Deleting tutorservice with ID: {id}")
            
            # Check if tutorservice exists
            existing = await TutorServiceDB.get_by_id(id)
            if not existing:
                logger.warning(f"TutorService with ID {id} not found for deletion")
                return False
            
            result = await TutorServiceDB.delete(id)
            logger.info(f"TutorService deleted successfully")
            return result
        except Exception as e:
            logger.error(f"Error deleting tutorservice: {str(e)}")
            raise
    
    @staticmethod
    async def validate_tutorservice_data(data: TutorServiceCreate) -> bool:
        """Validate tutorservice data before creation"""
        try:
            # Add custom validation logic here
            if not data.name or len(data.name.strip()) == 0:
                logger.warning("Invalid tutorservice data: name is required")
                return False
            
            # Add more validation rules as needed
            logger.info("TutorService data validation passed")
            return True
        except Exception as e:
            logger.error(f"Error validating tutorservice data: {str(e)}")
            return False
