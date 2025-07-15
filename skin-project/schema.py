from pydantic import BaseModel,Field
from typing import Literal



# define root endpoint response
class HomeResponse(BaseModel):
    """Pydantic object for the Home response modelling
    the root endpoint response object """
    message: str = Field(...,   description="server welcome message",
                         examples=["we are live"])


if __name__ == "__main__":
    pass