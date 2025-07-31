
from typing import List, Optional
from fileservice_model import FileServiceCreate, FileServiceUpdate, FileServiceInDB, FileServiceDB
import logging

logger = logging.getLogger(__name__)

class FileServiceService:
    """Service layer for FileService operations"""
    
    @staticmethod
    async def create_fileservice(data: FileServiceCreate) -> FileServiceInDB:
        """Create a new fileservice"""
        try:
            logger.info(f"Creating new fileservice: {data.name}")
            result = await FileServiceDB.create(data)
            logger.info(f"FileService created successfully with ID: {result.id}")
            return result
        except Exception as e:
            logger.error(f"Error creating fileservice: {str(e)}")
            raise
    
    @staticmethod
    async def get_fileservice_by_id(id: int) -> Optional[FileServiceInDB]:
        """Get fileservice by ID"""
        try:
            logger.info(f"Fetching fileservice with ID: {id}")
            result = await FileServiceDB.get_by_id(id)
            if not result:
                logger.warning(f"FileService with ID {id} not found")
            return result
        except Exception as e:
            logger.error(f"Error fetching fileservice: {str(e)}")
            raise
    
    @staticmethod
    async def get_all_fileservices() -> List[FileServiceInDB]:
        """Get all fileservices"""
        try:
            logger.info(f"Fetching all fileservices")
            result = await FileServiceDB.get_all()
            logger.info(f"Found {len(result)} fileservices")
            return result
        except Exception as e:
            logger.error(f"Error fetching fileservices: {str(e)}")
            raise
    
    @staticmethod
    async def update_fileservice(id: int, data: FileServiceUpdate) -> Optional[FileServiceInDB]:
        """Update fileservice by ID"""
        try:
            logger.info(f"Updating fileservice with ID: {id}")
            
            # Check if fileservice exists
            existing = await FileServiceDB.get_by_id(id)
            if not existing:
                logger.warning(f"FileService with ID {id} not found for update")
                return None
            
            result = await FileServiceDB.update(id, data)
            logger.info(f"FileService updated successfully")
            return result
        except Exception as e:
            logger.error(f"Error updating fileservice: {str(e)}")
            raise
    
    @staticmethod
    async def delete_fileservice(id: int) -> bool:
        """Delete fileservice by ID"""
        try:
            logger.info(f"Deleting fileservice with ID: {id}")
            
            # Check if fileservice exists
            existing = await FileServiceDB.get_by_id(id)
            if not existing:
                logger.warning(f"FileService with ID {id} not found for deletion")
                return False
            
            result = await FileServiceDB.delete(id)
            logger.info(f"FileService deleted successfully")
            return result
        except Exception as e:
            logger.error(f"Error deleting fileservice: {str(e)}")
            raise
    
    @staticmethod
    async def validate_fileservice_data(data: FileServiceCreate) -> bool:
        """Validate fileservice data before creation"""
        try:
            # Add custom validation logic here
            if not data.name or len(data.name.strip()) == 0:
                logger.warning("Invalid fileservice data: name is required")
                return False
            
            # Add more validation rules as needed
            logger.info("FileService data validation passed")
            return True
        except Exception as e:
            logger.error(f"Error validating fileservice data: {str(e)}")
            return False
