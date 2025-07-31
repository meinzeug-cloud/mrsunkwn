
from typing import List, Optional
from reportingservice_model import ReportingServiceCreate, ReportingServiceUpdate, ReportingServiceInDB, ReportingServiceDB
import logging

logger = logging.getLogger(__name__)

class ReportingServiceService:
    """Service layer for ReportingService operations"""
    
    @staticmethod
    async def create_reportingservice(data: ReportingServiceCreate) -> ReportingServiceInDB:
        """Create a new reportingservice"""
        try:
            logger.info(f"Creating new reportingservice: {data.name}")
            result = await ReportingServiceDB.create(data)
            logger.info(f"ReportingService created successfully with ID: {result.id}")
            return result
        except Exception as e:
            logger.error(f"Error creating reportingservice: {str(e)}")
            raise
    
    @staticmethod
    async def get_reportingservice_by_id(id: int) -> Optional[ReportingServiceInDB]:
        """Get reportingservice by ID"""
        try:
            logger.info(f"Fetching reportingservice with ID: {id}")
            result = await ReportingServiceDB.get_by_id(id)
            if not result:
                logger.warning(f"ReportingService with ID {id} not found")
            return result
        except Exception as e:
            logger.error(f"Error fetching reportingservice: {str(e)}")
            raise
    
    @staticmethod
    async def get_all_reportingservices() -> List[ReportingServiceInDB]:
        """Get all reportingservices"""
        try:
            logger.info(f"Fetching all reportingservices")
            result = await ReportingServiceDB.get_all()
            logger.info(f"Found {len(result)} reportingservices")
            return result
        except Exception as e:
            logger.error(f"Error fetching reportingservices: {str(e)}")
            raise
    
    @staticmethod
    async def update_reportingservice(id: int, data: ReportingServiceUpdate) -> Optional[ReportingServiceInDB]:
        """Update reportingservice by ID"""
        try:
            logger.info(f"Updating reportingservice with ID: {id}")
            
            # Check if reportingservice exists
            existing = await ReportingServiceDB.get_by_id(id)
            if not existing:
                logger.warning(f"ReportingService with ID {id} not found for update")
                return None
            
            result = await ReportingServiceDB.update(id, data)
            logger.info(f"ReportingService updated successfully")
            return result
        except Exception as e:
            logger.error(f"Error updating reportingservice: {str(e)}")
            raise
    
    @staticmethod
    async def delete_reportingservice(id: int) -> bool:
        """Delete reportingservice by ID"""
        try:
            logger.info(f"Deleting reportingservice with ID: {id}")
            
            # Check if reportingservice exists
            existing = await ReportingServiceDB.get_by_id(id)
            if not existing:
                logger.warning(f"ReportingService with ID {id} not found for deletion")
                return False
            
            result = await ReportingServiceDB.delete(id)
            logger.info(f"ReportingService deleted successfully")
            return result
        except Exception as e:
            logger.error(f"Error deleting reportingservice: {str(e)}")
            raise
    
    @staticmethod
    async def validate_reportingservice_data(data: ReportingServiceCreate) -> bool:
        """Validate reportingservice data before creation"""
        try:
            # Add custom validation logic here
            if not data.name or len(data.name.strip()) == 0:
                logger.warning("Invalid reportingservice data: name is required")
                return False
            
            # Add more validation rules as needed
            logger.info("ReportingService data validation passed")
            return True
        except Exception as e:
            logger.error(f"Error validating reportingservice data: {str(e)}")
            return False
