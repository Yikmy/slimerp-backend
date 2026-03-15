class AuditService:
    @staticmethod
    def log_login(user, company, request, success: bool, reason: str = ""):
        """
        Stub for Audit Service Login Log.
        Real implementation will write to LoginLog model.
        """
        # print(f"Audit Stub: Login user={user} success={success} reason={reason}")
        pass

    @staticmethod
    def log_action(actor, company, action, target, before=None, after=None, result=None):
        """
        Stub for Audit Service Action Log.
        Real implementation will write to AuditLog model.
        """
        # print(f"Audit Stub: Action {action} by {actor} on {target}")
        pass
