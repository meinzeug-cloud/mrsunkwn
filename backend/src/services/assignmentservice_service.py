
from typing import List, Optional
from assignmentservice_model import AssignmentServiceCreate, AssignmentServiceUpdate, AssignmentServiceInDB, AssignmentServiceDB
import logging

logger = logging.getLogger(__name__)

class AssignmentServiceService:
    """Service layer for AssignmentService operations"""
    
    @staticmethod
    async def create_assignmentservice(data: AssignmentServiceCreate) -> AssignmentServiceInDB:
        """Create a new assignmentservice"""
        try:
            logger.info(f"Creating new assignmentservice: {data.name}")
            result = await AssignmentServiceDB.create(data)
            logger.info(f"AssignmentService created successfully with ID: {result.id}")
            return result
        except Exception as e:
            logger.error(f"Error creating assignmentservice: {str(e)}")
            raise
    
    @staticmethod
    async def get_assignmentservice_by_id(id: int) -> Optional[AssignmentServiceInDB]:
        """Get assignmentservice by ID"""
        try:
            logger.info(f"Fetching assignmentservice with ID: {id}")
            result = await AssignmentServiceDB.get_by_id(id)
            if not result:
                logger.warning(f"AssignmentService with ID {id} not found")
            return result
        except Exception as e:
            logger.error(f"Error fetching assignmentservice: {str(e)}")
            raise
    
    @staticmethod
    async def get_all_assignmentservices() -> List[AssignmentServiceInDB]:
        """Get all assignmentservices"""
        try:
            logger.info(f"Fetching all assignmentservices")
            result = await AssignmentServiceDB.get_all()
            logger.info(f"Found {len(result)} assignmentservices")
            return result
        except Exception as e:
            logger.error(f"Error fetching assignmentservices: {str(e)}")
            raise
    
    @staticmethod
    async def update_assignmentservice(id: int, data: AssignmentServiceUpdate) -> Optional[AssignmentServiceInDB]:
        """Update assignmentservice by ID"""
        try:
            logger.info(f"Updating assignmentservice with ID: {id}")
            
            # Check if assignmentservice exists
            existing = await AssignmentServiceDB.get_by_id(id)
            if not existing:
                logger.warning(f"AssignmentService with ID {id} not found for update")
                return None
            
            result = await AssignmentServiceDB.update(id, data)
            logger.info(f"AssignmentService updated successfully")
            return result
        except Exception as e:
            logger.error(f"Error updating assignmentservice: {str(e)}")
            raise
    
    @staticmethod
    async def delete_assignmentservice(id: int) -> bool:
        """Delete assignmentservice by ID"""
        try:
            logger.info(f"Deleting assignmentservice with ID: {id}")
            
            # Check if assignmentservice exists
            existing = await AssignmentServiceDB.get_by_id(id)
            if not existing:
                logger.warning(f"AssignmentService with ID {id} not found for deletion")
                return False
            
            result = await AssignmentServiceDB.delete(id)
            logger.info(f"AssignmentService deleted successfully")
            return result
        except Exception as e:
            logger.error(f"Error deleting assignmentservice: {str(e)}")
            raise
    
    @staticmethod
    async def validate_assignmentservice_data(data: AssignmentServiceCreate) -> bool:
        """Validate assignmentservice data before creation"""
        try:
            # Add custom validation logic here
            if not data.name or len(data.name.strip()) == 0:
                logger.warning("Invalid assignmentservice data: name is required")
                return False
            
            # Add more validation rules as needed
            logger.info("AssignmentService data validation passed")
            return True
        except Exception as e:
            logger.error(f"Error validating assignmentservice data: {str(e)}")
            return False
