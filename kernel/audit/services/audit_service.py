import logging
from django.conf import settings
from kernel.audit.models import AuditLog, LoginLog

logger = logging.getLogger(__name__)

class AuditService:
    """
    Service for creating audit logs and login logs.
    """

    @staticmethod
    def log_action(
        actor,
        action,
        target_model,
        target_object_id,
        result=AuditLog.RESULT_SUCCESS,
        details=None,
        ip_address=None,
        user_agent=None,
        company=None
    ):
        """
        Logs a business action.
        
        :param actor: User instance who performed the action
        :param action: Action type (CREATE, UPDATE, DELETE, etc.)
        :param target_model: Name of the model being acted upon
        :param target_object_id: ID of the object being acted upon
        :param result: Result of the action (SUCCESS/FAILURE)
        :param details: Dictionary containing extra details
        :param ip_address: IP address of the request
        :param user_agent: User agent string
        :param company: Company instance context
        """
        try:
            # If actor is not a user instance (e.g. None or anonymous), handle gracefully
            user = actor if hasattr(actor, 'pk') else None

            AuditLog.objects.create(
                created_by=user,
                action=action,
                target_model=target_model,
                target_object_id=str(target_object_id),
                result=result,
                details=details or {},
                ip_address=ip_address,
                user_agent=user_agent,
                company=company
            )
        except Exception as e:
            # Audit logging failure should not block the main business logic
            logger.error(f"Failed to create audit log: {e}", exc_info=True)

    @staticmethod
    def log_login(
        username,
        status,
        user=None,
        ip_address=None,
        user_agent=None,
        failure_reason=None,
        company=None,
        details=None
    ):
        """
        Logs a login attempt.
        
        :param username: Username attempted
        :param status: SUCCESS or FAILURE
        :param user: User instance if identified (optional)
        :param ip_address: IP address of the request
        :param user_agent: User agent string
        :param failure_reason: Reason string if failed
        :param company: Company instance context
        :param details: Dictionary containing extra details
        """
        try:
            LoginLog.objects.create(
                user=user,
                username=username,
                status=status,
                ip_address=ip_address,
                user_agent=user_agent,
                failure_reason=failure_reason,
                company=company,
                details=details or {}
            )
        except Exception as e:
            logger.error(f"Failed to create login log: {e}", exc_info=True)
