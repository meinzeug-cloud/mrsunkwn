
from typing import List, Optional
from feedbackservice_model import FeedbackServiceCreate, FeedbackServiceUpdate, FeedbackServiceInDB, FeedbackServiceDB
import logging

logger = logging.getLogger(__name__)

class FeedbackServiceService:
    """Service layer for FeedbackService operations"""
    
    @staticmethod
    async def create_feedbackservice(data: FeedbackServiceCreate) -> FeedbackServiceInDB:
        """Create a new feedbackservice"""
        try:
            logger.info(f"Creating new feedbackservice: {data.name}")
            result = await FeedbackServiceDB.create(data)
            logger.info(f"FeedbackService created successfully with ID: {result.id}")
            return result
        except Exception as e:
            logger.error(f"Error creating feedbackservice: {str(e)}")
            raise
    
    @staticmethod
    async def get_feedbackservice_by_id(id: int) -> Optional[FeedbackServiceInDB]:
        """Get feedbackservice by ID"""
        try:
            logger.info(f"Fetching feedbackservice with ID: {id}")
            result = await FeedbackServiceDB.get_by_id(id)
            if not result:
                logger.warning(f"FeedbackService with ID {id} not found")
            return result
        except Exception as e:
            logger.error(f"Error fetching feedbackservice: {str(e)}")
            raise
    
    @staticmethod
    async def get_all_feedbackservices() -> List[FeedbackServiceInDB]:
        """Get all feedbackservices"""
        try:
            logger.info(f"Fetching all feedbackservices")
            result = await FeedbackServiceDB.get_all()
            logger.info(f"Found {len(result)} feedbackservices")
            return result
        except Exception as e:
            logger.error(f"Error fetching feedbackservices: {str(e)}")
            raise
    
    @staticmethod
    async def update_feedbackservice(id: int, data: FeedbackServiceUpdate) -> Optional[FeedbackServiceInDB]:
        """Update feedbackservice by ID"""
        try:
            logger.info(f"Updating feedbackservice with ID: {id}")
            
            # Check if feedbackservice exists
            existing = await FeedbackServiceDB.get_by_id(id)
            if not existing:
                logger.warning(f"FeedbackService with ID {id} not found for update")
                return None
            
            result = await FeedbackServiceDB.update(id, data)
            logger.info(f"FeedbackService updated successfully")
            return result
        except Exception as e:
            logger.error(f"Error updating feedbackservice: {str(e)}")
            raise
    
    @staticmethod
    async def delete_feedbackservice(id: int) -> bool:
        """Delete feedbackservice by ID"""
        try:
            logger.info(f"Deleting feedbackservice with ID: {id}")
            
            # Check if feedbackservice exists
            existing = await FeedbackServiceDB.get_by_id(id)
            if not existing:
                logger.warning(f"FeedbackService with ID {id} not found for deletion")
                return False
            
            result = await FeedbackServiceDB.delete(id)
            logger.info(f"FeedbackService deleted successfully")
            return result
        except Exception as e:
            logger.error(f"Error deleting feedbackservice: {str(e)}")
            raise
    
    @staticmethod
    async def validate_feedbackservice_data(data: FeedbackServiceCreate) -> bool:
        """Validate feedbackservice data before creation"""
        try:
            # Add custom validation logic here
            if not data.name or len(data.name.strip()) == 0:
                logger.warning("Invalid feedbackservice data: name is required")
                return False
            
            # Add more validation rules as needed
            logger.info("FeedbackService data validation passed")
            return True
        except Exception as e:
            logger.error(f"Error validating feedbackservice data: {str(e)}")
            return False
