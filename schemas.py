from pydantic import BaseModel, HttpUrl, Field
from typing import Optional
import random
import string

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class Redirect(BaseModel):
    short_str: str = Field(default_factory=id_generator)
    url: HttpUrl
    redirect_count: Optional[int] = 0
