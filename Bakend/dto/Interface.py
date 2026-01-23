from pydantic import BaseModel

class BaseDTO(BaseModel):
    class Config:
        orm_mode = True
        anystr_strip_whitespace = True

class ConvertDTO:
    def to_BaseDTO(self) -> BaseDTO:
        pass