
from typing import List, Optional
from authservice_model import AuthServiceCreate, AuthServiceUpdate, AuthServiceInDB, AuthServiceDB
import logging

logger = logging.getLogger(__name__)

class AuthServiceService:
    """Service layer for AuthService operations"""
    
    @staticmethod
    async def create_authservice(data: AuthServiceCreate) -> AuthServiceInDB:
        """Create a new authservice"""
        try:
            logger.info(f"Creating new authservice: {data.name}")
            result = await AuthServiceDB.create(data)
            logger.info(f"AuthService created successfully with ID: {result.id}")
            return result
        except Exception as e:
            logger.error(f"Error creating authservice: {str(e)}")
            raise
    
    @staticmethod
    async def get_authservice_by_id(id: int) -> Optional[AuthServiceInDB]:
        """Get authservice by ID"""
        try:
            logger.info(f"Fetching authservice with ID: {id}")
            result = await AuthServiceDB.get_by_id(id)
            if not result:
                logger.warning(f"AuthService with ID {id} not found")
            return result
        except Exception as e:
            logger.error(f"Error fetching authservice: {str(e)}")
            raise
    
    @staticmethod
    async def get_all_authservices() -> List[AuthServiceInDB]:
        """Get all authservices"""
        try:
            logger.info(f"Fetching all authservices")
            result = await AuthServiceDB.get_all()
            logger.info(f"Found {len(result)} authservices")
            return result
        except Exception as e:
            logger.error(f"Error fetching authservices: {str(e)}")
            raise
    
    @staticmethod
    async def update_authservice(id: int, data: AuthServiceUpdate) -> Optional[AuthServiceInDB]:
        """Update authservice by ID"""
        try:
            logger.info(f"Updating authservice with ID: {id}")
            
            # Check if authservice exists
            existing = await AuthServiceDB.get_by_id(id)
            if not existing:
                logger.warning(f"AuthService with ID {id} not found for update")
                return None
            
            result = await AuthServiceDB.update(id, data)
            logger.info(f"AuthService updated successfully")
            return result
        except Exception as e:
            logger.error(f"Error updating authservice: {str(e)}")
            raise
    
    @staticmethod
    async def delete_authservice(id: int) -> bool:
        """Delete authservice by ID"""
        try:
            logger.info(f"Deleting authservice with ID: {id}")
            
            # Check if authservice exists
            existing = await AuthServiceDB.get_by_id(id)
            if not existing:
                logger.warning(f"AuthService with ID {id} not found for deletion")
                return False
            
            result = await AuthServiceDB.delete(id)
            logger.info(f"AuthService deleted successfully")
            return result
        except Exception as e:
            logger.error(f"Error deleting authservice: {str(e)}")
            raise
    
    @staticmethod
    async def validate_authservice_data(data: AuthServiceCreate) -> bool:
        """Validate authservice data before creation"""
        try:
            # Add custom validation logic here
            if not data.name or len(data.name.strip()) == 0:
                logger.warning("Invalid authservice data: name is required")
                return False
            
            # Add more validation rules as needed
            logger.info("AuthService data validation passed")
            return True
        except Exception as e:
            logger.error(f"Error validating authservice data: {str(e)}")
            return False
