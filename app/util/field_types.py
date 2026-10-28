from typing import Annotated

from pydantic import Field

Port = Annotated[int, Field(ge=1, le=65535)]

