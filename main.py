from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
import schemas

app = FastAPI()

@app.get("/{short_str}")
def read_item(short_str: str):
    # TODO: check if exist, and redirect
    if short_str == "123":
        # TODO: increase redirect_count
        return RedirectResponse("https://google.com/")
    else:
        raise HTTPException(status_code=404, detail="Redirect not found")

@app.post("/redirects")
def crete_redirect(redirect: schemas.Redirect):
    return { "url": redirect.url, "short_str": redirect.short_str }