
from typing import List, Optional
from userservice_model import UserServiceCreate, UserServiceUpdate, UserServiceInDB, UserServiceDB
import logging

logger = logging.getLogger(__name__)

class UserServiceService:
    """Service layer for UserService operations"""
    
    @staticmethod
    async def create_userservice(data: UserServiceCreate) -> UserServiceInDB:
        """Create a new userservice"""
        try:
            logger.info(f"Creating new userservice: {data.name}")
            result = await UserServiceDB.create(data)
            logger.info(f"UserService created successfully with ID: {result.id}")
            return result
        except Exception as e:
            logger.error(f"Error creating userservice: {str(e)}")
            raise
    
    @staticmethod
    async def get_userservice_by_id(id: int) -> Optional[UserServiceInDB]:
        """Get userservice by ID"""
        try:
            logger.info(f"Fetching userservice with ID: {id}")
            result = await UserServiceDB.get_by_id(id)
            if not result:
                logger.warning(f"UserService with ID {id} not found")
            return result
        except Exception as e:
            logger.error(f"Error fetching userservice: {str(e)}")
            raise
    
    @staticmethod
    async def get_all_userservices() -> List[UserServiceInDB]:
        """Get all userservices"""
        try:
            logger.info(f"Fetching all userservices")
            result = await UserServiceDB.get_all()
            logger.info(f"Found {len(result)} userservices")
            return result
        except Exception as e:
            logger.error(f"Error fetching userservices: {str(e)}")
            raise
    
    @staticmethod
    async def update_userservice(id: int, data: UserServiceUpdate) -> Optional[UserServiceInDB]:
        """Update userservice by ID"""
        try:
            logger.info(f"Updating userservice with ID: {id}")
            
            # Check if userservice exists
            existing = await UserServiceDB.get_by_id(id)
            if not existing:
                logger.warning(f"UserService with ID {id} not found for update")
                return None
            
            result = await UserServiceDB.update(id, data)
            logger.info(f"UserService updated successfully")
            return result
        except Exception as e:
            logger.error(f"Error updating userservice: {str(e)}")
            raise
    
    @staticmethod
    async def delete_userservice(id: int) -> bool:
        """Delete userservice by ID"""
        try:
            logger.info(f"Deleting userservice with ID: {id}")
            
            # Check if userservice exists
            existing = await UserServiceDB.get_by_id(id)
            if not existing:
                logger.warning(f"UserService with ID {id} not found for deletion")
                return False
            
            result = await UserServiceDB.delete(id)
            logger.info(f"UserService deleted successfully")
            return result
        except Exception as e:
            logger.error(f"Error deleting userservice: {str(e)}")
            raise
    
    @staticmethod
    async def validate_userservice_data(data: UserServiceCreate) -> bool:
        """Validate userservice data before creation"""
        try:
            # Add custom validation logic here
            if not data.name or len(data.name.strip()) == 0:
                logger.warning("Invalid userservice data: name is required")
                return False
            
            # Add more validation rules as needed
            logger.info("UserService data validation passed")
            return True
        except Exception as e:
            logger.error(f"Error validating userservice data: {str(e)}")
            return False
