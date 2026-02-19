from pathlib import Path

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="devops-lab-app", version="0.2.0")

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

items: list[dict[str, str | int]] = []
next_id = 1


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
def read_index(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "items": items,
        },
    )


@app.post("/items")
def create_item(title: str = Form(...), description: str = Form("")):
    global next_id

    item = {
        "id": next_id,
        "title": title.strip(),
        "description": description.strip(),
    }
    items.append(item)
    next_id += 1

    return RedirectResponse(url="/", status_code=303)


@app.get("/items/{item_id}/edit")
def read_edit_item(request: Request, item_id: int):
    item = _get_item_or_404(item_id)
    return templates.TemplateResponse(request, "edit.html", {"item": item})


@app.post("/items/{item_id}/edit")
def update_item(item_id: int, title: str = Form(...), description: str = Form("")):
    item = _get_item_or_404(item_id)
    item["title"] = title.strip()
    item["description"] = description.strip()
    return RedirectResponse(url="/", status_code=303)


@app.post("/items/{item_id}/delete")
def delete_item(item_id: int):
    item = _get_item_or_404(item_id)
    items.remove(item)
    return RedirectResponse(url="/", status_code=303)


def _get_item_or_404(item_id: int) -> dict[str, str | int]:
    for item in items:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")
