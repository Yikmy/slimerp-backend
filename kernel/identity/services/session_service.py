class SessionService:
    @staticmethod
    def attach_session(response, user):
        """
        Helper to manage session/cookie on response if needed.
        Since Django's login() middleware handles session cookie setting automatically,
        this might be used for additional headers or custom cookie attributes.
        For now, it's a pass-through or placeholder as per spec requirement.
        """
        # In a standard Django session setup, the cookie is set by SessionMiddleware
        # when request.session is modified (which login() does).
        # So explicit attachment to response is usually not needed unless we are doing stateless tokens.
        # But complying with spec interface:
        pass
