from pydantic import BaseModel


class TestResponseSchema(BaseModel):
    id: int
    name: str
    description: str | None = None


class CreateTestSchema(BaseModel):
    name: str
    description: str | None = None


class UpdateTestSchema(BaseModel):
    name: str | None = None
    description: str | None = None
