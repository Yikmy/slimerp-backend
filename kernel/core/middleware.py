import threading
from django.utils.deprecation import MiddlewareMixin

_thread_locals = threading.local()

def get_current_company_id():
    return getattr(_thread_locals, 'company_id', None)

class CurrentCompanyMiddleware(MiddlewareMixin):
    """
    Middleware to extract company context from request headers
    and store it in thread-local storage for easy access.
    
    Header format: X-Company-ID: <uuid>
    """
    def process_request(self, request):
        company_id = request.headers.get('X-Company-ID')
        
        # Also check session if available (for browser clients)
        if not company_id and hasattr(request, 'session'):
             company_id = request.session.get('company_id')

        if company_id:
            request.company_id = company_id
            _thread_locals.company_id = company_id
        else:
            request.company_id = None
            if hasattr(_thread_locals, 'company_id'):
                del _thread_locals.company_id

    def process_response(self, request, response):
        # Clean up thread local
        if hasattr(_thread_locals, 'company_id'):
            del _thread_locals.company_id
        return response
