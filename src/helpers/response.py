from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

DataType = TypeVar("DataType")


class ResponseModel(BaseModel, Generic[DataType]):
    """
    Base model for API responses.
    """

    status_code: int
    message: str
    data: Optional[DataType] = None


def response(status_code: int, message: str, data: dict = None) -> dict:
    """
    Helper function to create a standardized response format.

    Args:
        status_code (int): HTTP status code.
        message (str): Message to include in the response.
        data (dict, optional): Additional data to include in the response.

    Returns:
        dict: A dictionary containing the status code, message, and data.
    """
    return {"status_code": status_code, "message": message, "data": data}
