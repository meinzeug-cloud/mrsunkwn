
import asyncio
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from models.devicemonitoring import (
    DeviceMonitoringCreate,
    DeviceMonitoringUpdate, 
    DeviceMonitoringInDB,
    DeviceMonitoringOperations,
    DeviceMonitoringAnalytics
)
from services.notification_service import NotificationService
from services.ai_tutor_service import AITutorService
from utils.monitoring import log_user_activity
from config import settings

logger = logging.getLogger(__name__)

class DeviceMonitoringService:
    """
    Mrs-Unkwn DeviceMonitoringService - Comprehensive service for devicemonitoring management
    
    This service handles all business logic related to devicemonitorings
    in the Mrs-Unkwn platform, including AI integration and parental controls.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.operations = DeviceMonitoringOperations(db)
        self.notification_service = NotificationService()
        self.ai_tutor_service = AITutorService(db)
        
    async def create_devicemonitoring(
        self, 
        data: DeviceMonitoringCreate, 
        user_id: str
    ) -> DeviceMonitoringInDB:
        """Create a new devicemonitoring with Mrs-Unkwn features"""
        try:
            logger.info(f"Creating devicemonitoring for user {user_id}: {data.name}")
            
            # Validate user permissions
            if not await self._validate_user_permissions(user_id, "create"):
                raise ValueError("User does not have permission to create devicemonitorings")
            
            # Check parental controls
            if data.requires_parent_approval:
                parent_approved = await self._check_parental_approval(user_id, data)
                if not parent_approved:
                    raise ValueError("Parental approval required for this devicemonitoring")
            
            # Create the devicemonitoring
            result = await self.operations.create(data)
            
            # Initialize AI tutor if enabled
            if data.ai_interaction_enabled:
                await self.ai_tutor_service.initialize_for_devicemonitoring(result.id)
            
            # Log activity
            await log_user_activity(
                user_id, 
                "create_devicemonitoring", 
                {"item_id": result.id, "name": data.name}
            )
            
            # Notify family members if configured
            await self._notify_family_of_creation(result)
            
            logger.info(f"DeviceMonitoring created successfully: {result.id}")
            return result
            
        except Exception as e:
            logger.error(f"Error creating devicemonitoring: {str(e)}")
            raise
    
    async def get_devicemonitoring_by_id(
        self, 
        item_id: str, 
        user_id: str,
        include_analytics: bool = True
    ) -> Optional[DeviceMonitoringInDB]:
        """Get devicemonitoring by ID with permission checks"""
        try:
            logger.info(f"Fetching devicemonitoring {item_id} for user {user_id}")
            
            # Get the item
            item = await self.operations.get_by_id(item_id)
            if not item:
                return None
            
            # Check access permissions
            if not await self._validate_access_permissions(user_id, item):
                raise ValueError("User does not have access to this devicemonitoring")
            
            # Add real-time analytics if requested
            if include_analytics:
                analytics = await self.operations.get_analytics(item.user_id)
                item.metadata["analytics"] = analytics.dict()
            
            # Log access
            await log_user_activity(
                user_id,
                "view_devicemonitoring",
                {"item_id": item_id}
            )
            
            return item
            
        except Exception as e:
            logger.error(f"Error fetching devicemonitoring: {str(e)}")
            raise
    
    async def get_user_devicemonitorings(
        self,
        user_id: str,
        filters: Dict[str, Any] = None,
        page: int = 1,
        per_page: int = 20
    ) -> List[DeviceMonitoringInDB]:
        """Get devicemonitorings for a user with filtering"""
        try:
            logger.info(f"Fetching devicemonitorings for user {user_id}")
            
            # Apply filters and get items
            result = await self.operations.get_by_user(user_id, page, per_page)
            
            # Apply additional Mrs-Unkwn filters
            if filters:
                result = await self._apply_mrs_unkwn_filters(result, filters)
            
            # Log activity
            await log_user_activity(
                user_id,
                "list_devicemonitorings",
                {"count": len(result.items), "filters": filters}
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error fetching user devicemonitorings: {str(e)}")
            raise
    
    async def update_devicemonitoring(
        self,
        item_id: str,
        data: DeviceMonitoringUpdate,
        user_id: str
    ) -> Optional[DeviceMonitoringInDB]:
        """Update devicemonitoring with permission checks"""
        try:
            logger.info(f"Updating devicemonitoring {item_id} for user {user_id}")
            
            # Get existing item
            existing = await self.operations.get_by_id(item_id)
            if not existing:
                return None
            
            # Check update permissions
            if not await self._validate_update_permissions(user_id, existing):
                raise ValueError("User does not have permission to update this devicemonitoring")
            
            # Check if parental approval needed for changes
            if await self._requires_parental_approval_for_update(existing, data):
                parent_approved = await self._check_parental_approval_for_update(user_id, existing, data)
                if not parent_approved:
                    raise ValueError("Parental approval required for these changes")
            
            # Update the item
            result = await self.operations.update(item_id, data)
            
            # Update AI tutor configuration if needed
            if data.ai_interaction_enabled is not None:
                if data.ai_interaction_enabled:
                    await self.ai_tutor_service.initialize_for_devicemonitoring(item_id)
                else:
                    await self.ai_tutor_service.disable_for_devicemonitoring(item_id)
            
            # Log activity
            await log_user_activity(
                user_id,
                "update_devicemonitoring",
                {"item_id": item_id, "changes": data.dict(exclude_unset=True)}
            )
            
            # Notify family of significant changes
            await self._notify_family_of_update(result, data)
            
            logger.info(f"DeviceMonitoring updated successfully: {item_id}")
            return result
            
        except Exception as e:
            logger.error(f"Error updating devicemonitoring: {str(e)}")
            raise
    
    async def delete_devicemonitoring(
        self,
        item_id: str,
        user_id: str,
        force: bool = False
    ) -> bool:
        """Delete devicemonitoring with permission checks"""
        try:
            logger.info(f"Deleting devicemonitoring {item_id} for user {user_id}")
            
            # Get existing item
            existing = await self.operations.get_by_id(item_id)
            if not existing:
                return False
            
            # Check delete permissions
            if not await self._validate_delete_permissions(user_id, existing):
                raise ValueError("User does not have permission to delete this devicemonitoring")
            
            # Check if parental approval needed for deletion
            if not force and existing.requires_parent_approval:
                parent_approved = await self._check_parental_approval_for_deletion(user_id, existing)
                if not parent_approved:
                    raise ValueError("Parental approval required for deletion")
            
            # Cleanup AI tutor integration
            await self.ai_tutor_service.cleanup_for_devicemonitoring(item_id)
            
            # Delete the item
            success = await self.operations.delete(item_id)
            
            if success:
                # Log activity
                await log_user_activity(
                    user_id,
                    "delete_devicemonitoring",
                    {"item_id": item_id, "force": force}
                )
                
                # Notify family of deletion
                await self._notify_family_of_deletion(existing)
                
                logger.info(f"DeviceMonitoring deleted successfully: {item_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error deleting devicemonitoring: {str(e)}")
            raise
    
    async def get_analytics(
        self,
        user_id: str,
        timeframe: str = "week"
    ) -> DeviceMonitoringAnalytics:
        """Get comprehensive analytics for user's devicemonitorings"""
        try:
            logger.info(f"Generating analytics for user {user_id} over {timeframe}")
            
            analytics = await self.operations.get_analytics(user_id, timeframe)
            
            # Add Mrs-Unkwn specific analytics
            enhanced_analytics = await self._enhance_analytics_with_ai_insights(analytics)
            
            # Log analytics access
            await log_user_activity(
                user_id,
                "view_analytics",
                {"timeframe": timeframe, "type": "devicemonitoring_analytics"}
            )
            
            return enhanced_analytics
            
        except Exception as e:
            logger.error(f"Error generating analytics: {str(e)}")
            raise
    
    # Private helper methods
    async def _validate_user_permissions(self, user_id: str, action: str) -> bool:
        """Validate user permissions for actions"""
        # Implementation would check user roles, family settings, etc.
        return True
    
    async def _validate_access_permissions(self, user_id: str, item: DeviceMonitoringInDB) -> bool:
        """Validate user can access specific item"""
        # Check if user owns the item or has family access
        return item.user_id == user_id or await self._has_family_access(user_id, item.family_id)
    
    async def _validate_update_permissions(self, user_id: str, item: DeviceMonitoringInDB) -> bool:
        """Validate user can update specific item"""
        return await self._validate_access_permissions(user_id, item)
    
    async def _validate_delete_permissions(self, user_id: str, item: DeviceMonitoringInDB) -> bool:
        """Validate user can delete specific item"""
        return await self._validate_access_permissions(user_id, item)
    
    async def _has_family_access(self, user_id: str, family_id: str) -> bool:
        """Check if user has access to family resources"""
        # Implementation would check family membership
        return True
    
    async def _check_parental_approval(self, user_id: str, data: DeviceMonitoringCreate) -> bool:
        """Check if parental approval is granted"""
        # Implementation would check parental control settings
        return True
    
    async def _check_parental_approval_for_update(self, user_id: str, existing: DeviceMonitoringInDB, data: DeviceMonitoringUpdate) -> bool:
        """Check parental approval for updates"""
        return True
    
    async def _check_parental_approval_for_deletion(self, user_id: str, existing: DeviceMonitoringInDB) -> bool:
        """Check parental approval for deletion"""
        return True
    
    async def _requires_parental_approval_for_update(self, existing: DeviceMonitoringInDB, data: DeviceMonitoringUpdate) -> bool:
        """Check if update requires parental approval"""
        # Check if significant fields are being changed
        significant_changes = ['difficulty_level', 'subject_areas', 'ai_interaction_enabled']
        for field in significant_changes:
            if getattr(data, field, None) is not None:
                return True
        return False
    
    async def _apply_mrs_unkwn_filters(self, result, filters: Dict[str, Any]):
        """Apply Mrs-Unkwn specific filters"""
        # Implementation would apply filters like subject, difficulty, etc.
        return result
    
    async def _notify_family_of_creation(self, item: DeviceMonitoringInDB):
        """Notify family members of new item creation"""
        await self.notification_service.notify_family(
            item.family_id,
            f"New devicemonitoring created: {item.name}",
            {"type": "creation", "item_id": item.id}
        )
    
    async def _notify_family_of_update(self, item: DeviceMonitoringInDB, changes: DeviceMonitoringUpdate):
        """Notify family members of item updates"""
        if any(getattr(changes, field, None) is not None for field in ['difficulty_level', 'subject_areas']):
            await self.notification_service.notify_family(
                item.family_id,
                f"DeviceMonitoring updated: {item.name}",
                {"type": "update", "item_id": item.id, "changes": changes.dict(exclude_unset=True)}
            )
    
    async def _notify_family_of_deletion(self, item: DeviceMonitoringInDB):
        """Notify family members of item deletion"""
        await self.notification_service.notify_family(
            item.family_id,
            f"DeviceMonitoring deleted: {item.name}",
            {"type": "deletion", "item_id": item.id}
        )
    
    async def _enhance_analytics_with_ai_insights(self, analytics: DeviceMonitoringAnalytics) -> DeviceMonitoringAnalytics:
        """Enhance analytics with AI-powered insights"""
        # Add AI-generated insights and recommendations
        ai_insights = await self.ai_tutor_service.generate_analytics_insights(analytics)
        analytics.recommendations.extend(ai_insights.get('recommendations', []))
        return analytics
