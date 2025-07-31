
from typing import List, Optional
from emailservice_model import EmailServiceCreate, EmailServiceUpdate, EmailServiceInDB, EmailServiceDB
import logging

logger = logging.getLogger(__name__)

class EmailServiceService:
    """Service layer for EmailService operations"""
    
    @staticmethod
    async def create_emailservice(data: EmailServiceCreate) -> EmailServiceInDB:
        """Create a new emailservice"""
        try:
            logger.info(f"Creating new emailservice: {data.name}")
            result = await EmailServiceDB.create(data)
            logger.info(f"EmailService created successfully with ID: {result.id}")
            return result
        except Exception as e:
            logger.error(f"Error creating emailservice: {str(e)}")
            raise
    
    @staticmethod
    async def get_emailservice_by_id(id: int) -> Optional[EmailServiceInDB]:
        """Get emailservice by ID"""
        try:
            logger.info(f"Fetching emailservice with ID: {id}")
            result = await EmailServiceDB.get_by_id(id)
            if not result:
                logger.warning(f"EmailService with ID {id} not found")
            return result
        except Exception as e:
            logger.error(f"Error fetching emailservice: {str(e)}")
            raise
    
    @staticmethod
    async def get_all_emailservices() -> List[EmailServiceInDB]:
        """Get all emailservices"""
        try:
            logger.info(f"Fetching all emailservices")
            result = await EmailServiceDB.get_all()
            logger.info(f"Found {len(result)} emailservices")
            return result
        except Exception as e:
            logger.error(f"Error fetching emailservices: {str(e)}")
            raise
    
    @staticmethod
    async def update_emailservice(id: int, data: EmailServiceUpdate) -> Optional[EmailServiceInDB]:
        """Update emailservice by ID"""
        try:
            logger.info(f"Updating emailservice with ID: {id}")
            
            # Check if emailservice exists
            existing = await EmailServiceDB.get_by_id(id)
            if not existing:
                logger.warning(f"EmailService with ID {id} not found for update")
                return None
            
            result = await EmailServiceDB.update(id, data)
            logger.info(f"EmailService updated successfully")
            return result
        except Exception as e:
            logger.error(f"Error updating emailservice: {str(e)}")
            raise
    
    @staticmethod
    async def delete_emailservice(id: int) -> bool:
        """Delete emailservice by ID"""
        try:
            logger.info(f"Deleting emailservice with ID: {id}")
            
            # Check if emailservice exists
            existing = await EmailServiceDB.get_by_id(id)
            if not existing:
                logger.warning(f"EmailService with ID {id} not found for deletion")
                return False
            
            result = await EmailServiceDB.delete(id)
            logger.info(f"EmailService deleted successfully")
            return result
        except Exception as e:
            logger.error(f"Error deleting emailservice: {str(e)}")
            raise
    
    @staticmethod
    async def validate_emailservice_data(data: EmailServiceCreate) -> bool:
        """Validate emailservice data before creation"""
        try:
            # Add custom validation logic here
            if not data.name or len(data.name.strip()) == 0:
                logger.warning("Invalid emailservice data: name is required")
                return False
            
            # Add more validation rules as needed
            logger.info("EmailService data validation passed")
            return True
        except Exception as e:
            logger.error(f"Error validating emailservice data: {str(e)}")
            return False
