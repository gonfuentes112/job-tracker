from pydantic import BaseModel, Field, ConfigDict


class ApplicationCreate(BaseModel):
    company: str = Field(min_length=1, max_length=255)
    role: str = Field(min_length=1, max_length=255)
    location: str = Field(min_length=1, max_length=255)


class ApplicationUpdate(BaseModel):
    company: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )
    role: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )
    status: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
    )
    location: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )


class ApplicationResponse(BaseModel):
    id: int
    company: str
    role: str
    status: str
    location: str

    model_config = ConfigDict(from_attributes=True)
