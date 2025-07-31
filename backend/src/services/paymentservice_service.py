
from typing import List, Optional
from paymentservice_model import PaymentServiceCreate, PaymentServiceUpdate, PaymentServiceInDB, PaymentServiceDB
import logging

logger = logging.getLogger(__name__)

class PaymentServiceService:
    """Service layer for PaymentService operations"""
    
    @staticmethod
    async def create_paymentservice(data: PaymentServiceCreate) -> PaymentServiceInDB:
        """Create a new paymentservice"""
        try:
            logger.info(f"Creating new paymentservice: {data.name}")
            result = await PaymentServiceDB.create(data)
            logger.info(f"PaymentService created successfully with ID: {result.id}")
            return result
        except Exception as e:
            logger.error(f"Error creating paymentservice: {str(e)}")
            raise
    
    @staticmethod
    async def get_paymentservice_by_id(id: int) -> Optional[PaymentServiceInDB]:
        """Get paymentservice by ID"""
        try:
            logger.info(f"Fetching paymentservice with ID: {id}")
            result = await PaymentServiceDB.get_by_id(id)
            if not result:
                logger.warning(f"PaymentService with ID {id} not found")
            return result
        except Exception as e:
            logger.error(f"Error fetching paymentservice: {str(e)}")
            raise
    
    @staticmethod
    async def get_all_paymentservices() -> List[PaymentServiceInDB]:
        """Get all paymentservices"""
        try:
            logger.info(f"Fetching all paymentservices")
            result = await PaymentServiceDB.get_all()
            logger.info(f"Found {len(result)} paymentservices")
            return result
        except Exception as e:
            logger.error(f"Error fetching paymentservices: {str(e)}")
            raise
    
    @staticmethod
    async def update_paymentservice(id: int, data: PaymentServiceUpdate) -> Optional[PaymentServiceInDB]:
        """Update paymentservice by ID"""
        try:
            logger.info(f"Updating paymentservice with ID: {id}")
            
            # Check if paymentservice exists
            existing = await PaymentServiceDB.get_by_id(id)
            if not existing:
                logger.warning(f"PaymentService with ID {id} not found for update")
                return None
            
            result = await PaymentServiceDB.update(id, data)
            logger.info(f"PaymentService updated successfully")
            return result
        except Exception as e:
            logger.error(f"Error updating paymentservice: {str(e)}")
            raise
    
    @staticmethod
    async def delete_paymentservice(id: int) -> bool:
        """Delete paymentservice by ID"""
        try:
            logger.info(f"Deleting paymentservice with ID: {id}")
            
            # Check if paymentservice exists
            existing = await PaymentServiceDB.get_by_id(id)
            if not existing:
                logger.warning(f"PaymentService with ID {id} not found for deletion")
                return False
            
            result = await PaymentServiceDB.delete(id)
            logger.info(f"PaymentService deleted successfully")
            return result
        except Exception as e:
            logger.error(f"Error deleting paymentservice: {str(e)}")
            raise
    
    @staticmethod
    async def validate_paymentservice_data(data: PaymentServiceCreate) -> bool:
        """Validate paymentservice data before creation"""
        try:
            # Add custom validation logic here
            if not data.name or len(data.name.strip()) == 0:
                logger.warning("Invalid paymentservice data: name is required")
                return False
            
            # Add more validation rules as needed
            logger.info("PaymentService data validation passed")
            return True
        except Exception as e:
            logger.error(f"Error validating paymentservice data: {str(e)}")
            return False
