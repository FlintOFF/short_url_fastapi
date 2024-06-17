from typing import Union, Optional

from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

import random
import string

app = FastAPI()

# TODO:
# GET redirect if url in the list
# POST create a new record

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
    
class Redirect(BaseModel):
    id: Optional[str] = None
    url: HttpUrl
    redirect_count: Optional[int] = 0

@app.get("/{redirect_id}")
def read_item(redirect_id: int):
    # TODO: check if exist, increase redirect_count, and redirect
    return {"item_id": redirect_id}

@app.post("/redirects")
def crete_redirect(redirect: Redirect):
    if redirect.id is None:
        redirect.id = id_generator()

    return { "url": redirect.url, "id": redirect.id }