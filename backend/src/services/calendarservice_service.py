
from typing import List, Optional
from calendarservice_model import CalendarServiceCreate, CalendarServiceUpdate, CalendarServiceInDB, CalendarServiceDB
import logging

logger = logging.getLogger(__name__)

class CalendarServiceService:
    """Service layer for CalendarService operations"""
    
    @staticmethod
    async def create_calendarservice(data: CalendarServiceCreate) -> CalendarServiceInDB:
        """Create a new calendarservice"""
        try:
            logger.info(f"Creating new calendarservice: {data.name}")
            result = await CalendarServiceDB.create(data)
            logger.info(f"CalendarService created successfully with ID: {result.id}")
            return result
        except Exception as e:
            logger.error(f"Error creating calendarservice: {str(e)}")
            raise
    
    @staticmethod
    async def get_calendarservice_by_id(id: int) -> Optional[CalendarServiceInDB]:
        """Get calendarservice by ID"""
        try:
            logger.info(f"Fetching calendarservice with ID: {id}")
            result = await CalendarServiceDB.get_by_id(id)
            if not result:
                logger.warning(f"CalendarService with ID {id} not found")
            return result
        except Exception as e:
            logger.error(f"Error fetching calendarservice: {str(e)}")
            raise
    
    @staticmethod
    async def get_all_calendarservices() -> List[CalendarServiceInDB]:
        """Get all calendarservices"""
        try:
            logger.info(f"Fetching all calendarservices")
            result = await CalendarServiceDB.get_all()
            logger.info(f"Found {len(result)} calendarservices")
            return result
        except Exception as e:
            logger.error(f"Error fetching calendarservices: {str(e)}")
            raise
    
    @staticmethod
    async def update_calendarservice(id: int, data: CalendarServiceUpdate) -> Optional[CalendarServiceInDB]:
        """Update calendarservice by ID"""
        try:
            logger.info(f"Updating calendarservice with ID: {id}")
            
            # Check if calendarservice exists
            existing = await CalendarServiceDB.get_by_id(id)
            if not existing:
                logger.warning(f"CalendarService with ID {id} not found for update")
                return None
            
            result = await CalendarServiceDB.update(id, data)
            logger.info(f"CalendarService updated successfully")
            return result
        except Exception as e:
            logger.error(f"Error updating calendarservice: {str(e)}")
            raise
    
    @staticmethod
    async def delete_calendarservice(id: int) -> bool:
        """Delete calendarservice by ID"""
        try:
            logger.info(f"Deleting calendarservice with ID: {id}")
            
            # Check if calendarservice exists
            existing = await CalendarServiceDB.get_by_id(id)
            if not existing:
                logger.warning(f"CalendarService with ID {id} not found for deletion")
                return False
            
            result = await CalendarServiceDB.delete(id)
            logger.info(f"CalendarService deleted successfully")
            return result
        except Exception as e:
            logger.error(f"Error deleting calendarservice: {str(e)}")
            raise
    
    @staticmethod
    async def validate_calendarservice_data(data: CalendarServiceCreate) -> bool:
        """Validate calendarservice data before creation"""
        try:
            # Add custom validation logic here
            if not data.name or len(data.name.strip()) == 0:
                logger.warning("Invalid calendarservice data: name is required")
                return False
            
            # Add more validation rules as needed
            logger.info("CalendarService data validation passed")
            return True
        except Exception as e:
            logger.error(f"Error validating calendarservice data: {str(e)}")
            return False
