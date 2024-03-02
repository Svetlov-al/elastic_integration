from datetime import date

from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    name: str
    surname: str | None
    date_of_birth: date | None
    interests: list[str] | None
