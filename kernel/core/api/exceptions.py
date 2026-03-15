from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from django.core.exceptions import PermissionDenied
from django.http import Http404
from kernel.core.exceptions import BusinessError
from .responses import error_response

def core_exception_handler(exc, context):
    """
    Custom exception handler that wraps DRF exceptions and BusinessErrors 
    into standard APIResponse format.
    """
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if isinstance(exc, BusinessError):
        return error_response(
            message=exc.message,
            code=exc.code,
            data=exc.details,
            status=400  # Default to 400 for business errors
        )

    if response is not None:
        # Standard DRF exception
        # We want to format it as our standard response
        # Usually response.data is a dict or list of errors
        
        code = "API_ERROR"
        message = "Request failed"
        
        if isinstance(exc, APIException):
             if hasattr(exc, 'default_code'):
                 code = str(exc.default_code).upper()
             if hasattr(exc, 'detail'):
                 # If detail is a string, use it as message
                 if isinstance(exc.detail, str):
                     message = exc.detail
                 # If detail is a list/dict (validation errors), keep generic message
                 else:
                     message = "Validation error"

        # Check specifically for 401/403/404 to map codes
        if response.status_code == 401:
            code = "UNAUTHORIZED"
        elif response.status_code == 403:
            code = "FORBIDDEN"
        elif response.status_code == 404:
            code = "NOT_FOUND"

        return error_response(
            message=message,
            code=code,
            data=response.data,
            status=response.status_code
        )

    return response
