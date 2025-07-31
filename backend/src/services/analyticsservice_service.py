
from typing import List, Optional
from analyticsservice_model import AnalyticsServiceCreate, AnalyticsServiceUpdate, AnalyticsServiceInDB, AnalyticsServiceDB
import logging

logger = logging.getLogger(__name__)

class AnalyticsServiceService:
    """Service layer for AnalyticsService operations"""
    
    @staticmethod
    async def create_analyticsservice(data: AnalyticsServiceCreate) -> AnalyticsServiceInDB:
        """Create a new analyticsservice"""
        try:
            logger.info(f"Creating new analyticsservice: {data.name}")
            result = await AnalyticsServiceDB.create(data)
            logger.info(f"AnalyticsService created successfully with ID: {result.id}")
            return result
        except Exception as e:
            logger.error(f"Error creating analyticsservice: {str(e)}")
            raise
    
    @staticmethod
    async def get_analyticsservice_by_id(id: int) -> Optional[AnalyticsServiceInDB]:
        """Get analyticsservice by ID"""
        try:
            logger.info(f"Fetching analyticsservice with ID: {id}")
            result = await AnalyticsServiceDB.get_by_id(id)
            if not result:
                logger.warning(f"AnalyticsService with ID {id} not found")
            return result
        except Exception as e:
            logger.error(f"Error fetching analyticsservice: {str(e)}")
            raise
    
    @staticmethod
    async def get_all_analyticsservices() -> List[AnalyticsServiceInDB]:
        """Get all analyticsservices"""
        try:
            logger.info(f"Fetching all analyticsservices")
            result = await AnalyticsServiceDB.get_all()
            logger.info(f"Found {len(result)} analyticsservices")
            return result
        except Exception as e:
            logger.error(f"Error fetching analyticsservices: {str(e)}")
            raise
    
    @staticmethod
    async def update_analyticsservice(id: int, data: AnalyticsServiceUpdate) -> Optional[AnalyticsServiceInDB]:
        """Update analyticsservice by ID"""
        try:
            logger.info(f"Updating analyticsservice with ID: {id}")
            
            # Check if analyticsservice exists
            existing = await AnalyticsServiceDB.get_by_id(id)
            if not existing:
                logger.warning(f"AnalyticsService with ID {id} not found for update")
                return None
            
            result = await AnalyticsServiceDB.update(id, data)
            logger.info(f"AnalyticsService updated successfully")
            return result
        except Exception as e:
            logger.error(f"Error updating analyticsservice: {str(e)}")
            raise
    
    @staticmethod
    async def delete_analyticsservice(id: int) -> bool:
        """Delete analyticsservice by ID"""
        try:
            logger.info(f"Deleting analyticsservice with ID: {id}")
            
            # Check if analyticsservice exists
            existing = await AnalyticsServiceDB.get_by_id(id)
            if not existing:
                logger.warning(f"AnalyticsService with ID {id} not found for deletion")
                return False
            
            result = await AnalyticsServiceDB.delete(id)
            logger.info(f"AnalyticsService deleted successfully")
            return result
        except Exception as e:
            logger.error(f"Error deleting analyticsservice: {str(e)}")
            raise
    
    @staticmethod
    async def validate_analyticsservice_data(data: AnalyticsServiceCreate) -> bool:
        """Validate analyticsservice data before creation"""
        try:
            # Add custom validation logic here
            if not data.name or len(data.name.strip()) == 0:
                logger.warning("Invalid analyticsservice data: name is required")
                return False
            
            # Add more validation rules as needed
            logger.info("AnalyticsService data validation passed")
            return True
        except Exception as e:
            logger.error(f"Error validating analyticsservice data: {str(e)}")
            return False
