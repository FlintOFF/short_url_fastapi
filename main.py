from fastapi import FastAPI
import schemas

app = FastAPI()

# TODO:
# GET redirect if url in the list
# POST create a new record

@app.get("/{short_str}")
def read_item(short_str: str):
    # TODO: check if exist, increase redirect_count, and redirect
    return {"item_id": short_str}

@app.post("/redirects")
def crete_redirect(redirect: schemas.Redirect):
    return { "url": redirect.url, "short_str": redirect.short_str }