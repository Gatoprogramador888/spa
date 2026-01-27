from pydantic import BaseModel
from pydantic import BaseModel, ConfigDict

class BaseDTO(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True
    )

class ConvertDTO:
    def to_BaseDTO(self) -> BaseDTO:
        pass