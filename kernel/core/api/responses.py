from rest_framework.response import Response
from typing import Any, Optional

class APIResponse(Response):
    """
    Standard API Response wrapper.
    Format:
    {
        "success": bool,
        "code": str,
        "message": str,
        "data": any
    }
    """
    def __init__(
        self, 
        data: Any = None, 
        success: bool = True, 
        code: str = "OK", 
        message: str = "", 
        status: int = 200, 
        headers: Optional[dict] = None,
        exception: bool = False,
        content_type: Optional[str] = None
    ):
        payload = {
            "success": success,
            "code": code,
            "message": message,
            "data": data
        }
        super().__init__(data=payload, status=status, template_name=None, headers=headers, exception=exception, content_type=content_type)

def success_response(data: Any = None, message: str = "", code: str = "OK", status: int = 200) -> APIResponse:
    return APIResponse(data=data, success=True, code=code, message=message, status=status)

def error_response(message: str, code: str = "ERROR", data: Any = None, status: int = 400) -> APIResponse:
    return APIResponse(data=data, success=False, code=code, message=message, status=status)
