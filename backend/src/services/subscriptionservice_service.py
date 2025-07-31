
from typing import List, Optional
from subscriptionservice_model import SubscriptionServiceCreate, SubscriptionServiceUpdate, SubscriptionServiceInDB, SubscriptionServiceDB
import logging

logger = logging.getLogger(__name__)

class SubscriptionServiceService:
    """Service layer for SubscriptionService operations"""
    
    @staticmethod
    async def create_subscriptionservice(data: SubscriptionServiceCreate) -> SubscriptionServiceInDB:
        """Create a new subscriptionservice"""
        try:
            logger.info(f"Creating new subscriptionservice: {data.name}")
            result = await SubscriptionServiceDB.create(data)
            logger.info(f"SubscriptionService created successfully with ID: {result.id}")
            return result
        except Exception as e:
            logger.error(f"Error creating subscriptionservice: {str(e)}")
            raise
    
    @staticmethod
    async def get_subscriptionservice_by_id(id: int) -> Optional[SubscriptionServiceInDB]:
        """Get subscriptionservice by ID"""
        try:
            logger.info(f"Fetching subscriptionservice with ID: {id}")
            result = await SubscriptionServiceDB.get_by_id(id)
            if not result:
                logger.warning(f"SubscriptionService with ID {id} not found")
            return result
        except Exception as e:
            logger.error(f"Error fetching subscriptionservice: {str(e)}")
            raise
    
    @staticmethod
    async def get_all_subscriptionservices() -> List[SubscriptionServiceInDB]:
        """Get all subscriptionservices"""
        try:
            logger.info(f"Fetching all subscriptionservices")
            result = await SubscriptionServiceDB.get_all()
            logger.info(f"Found {len(result)} subscriptionservices")
            return result
        except Exception as e:
            logger.error(f"Error fetching subscriptionservices: {str(e)}")
            raise
    
    @staticmethod
    async def update_subscriptionservice(id: int, data: SubscriptionServiceUpdate) -> Optional[SubscriptionServiceInDB]:
        """Update subscriptionservice by ID"""
        try:
            logger.info(f"Updating subscriptionservice with ID: {id}")
            
            # Check if subscriptionservice exists
            existing = await SubscriptionServiceDB.get_by_id(id)
            if not existing:
                logger.warning(f"SubscriptionService with ID {id} not found for update")
                return None
            
            result = await SubscriptionServiceDB.update(id, data)
            logger.info(f"SubscriptionService updated successfully")
            return result
        except Exception as e:
            logger.error(f"Error updating subscriptionservice: {str(e)}")
            raise
    
    @staticmethod
    async def delete_subscriptionservice(id: int) -> bool:
        """Delete subscriptionservice by ID"""
        try:
            logger.info(f"Deleting subscriptionservice with ID: {id}")
            
            # Check if subscriptionservice exists
            existing = await SubscriptionServiceDB.get_by_id(id)
            if not existing:
                logger.warning(f"SubscriptionService with ID {id} not found for deletion")
                return False
            
            result = await SubscriptionServiceDB.delete(id)
            logger.info(f"SubscriptionService deleted successfully")
            return result
        except Exception as e:
            logger.error(f"Error deleting subscriptionservice: {str(e)}")
            raise
    
    @staticmethod
    async def validate_subscriptionservice_data(data: SubscriptionServiceCreate) -> bool:
        """Validate subscriptionservice data before creation"""
        try:
            # Add custom validation logic here
            if not data.name or len(data.name.strip()) == 0:
                logger.warning("Invalid subscriptionservice data: name is required")
                return False
            
            # Add more validation rules as needed
            logger.info("SubscriptionService data validation passed")
            return True
        except Exception as e:
            logger.error(f"Error validating subscriptionservice data: {str(e)}")
            return False
