from typing import Any, Optional
from pydantic import BaseModel


class SuccessResponse(BaseModel):
    success: bool = True
    message: str
    data: Optional[Any] = None


def success(message: str = "Success", data: Any = None) -> dict:
    return {"success": True, "message": message, "data": data}


def error(message: str, error_code: str = "ERROR") -> dict:
    return {"success": False, "error": message, "error_code": error_code}
