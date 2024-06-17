from typing import Union, Optional

from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl, Field

import random
import string

app = FastAPI()

# TODO:
# GET redirect if url in the list
# POST create a new record

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
    
class Redirect(BaseModel):
    short_str: str = Field(default_factory=id_generator)
    url: HttpUrl
    redirect_count: Optional[int] = 0

@app.get("/{short_str}")
def read_item(short_str: str):
    # TODO: check if exist, increase redirect_count, and redirect
    return {"item_id": short_str}

@app.post("/redirects")
def crete_redirect(redirect: Redirect):
    return { "url": redirect.url, "short_str": redirect.short_str }