from pydantic import BaseModel, field_validator


class MessageA(BaseModel):
    messageA:str

    @field_validator("messageA")
    @classmethod
    def validate_message(cls, v: str):
        if not v or not v.strip():
            raise ValueError("messageA 不能为空")
        if len(v) < 10:
            raise ValueError("messageA 长度不能小于 10")
        if len(v) > 15:
            raise ValueError("messageA 长度不能大于 15")
        return v

class Saves(BaseModel):
    type:str
    content:str