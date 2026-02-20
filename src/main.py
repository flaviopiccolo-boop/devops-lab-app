from contextlib import asynccontextmanager
import os
import time
from pathlib import Path

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine, delete, insert, select, update
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

@asynccontextmanager
async def lifespan(_: FastAPI):
    _initialize_database()
    yield


app = FastAPI(title="devops-lab-app", version="0.3.0", lifespan=lifespan)

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

metadata = MetaData()
items_table = Table(
    "items",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String(255), nullable=False),
    Column("description", String(1024), nullable=False, default=""),
)


def _resolve_database_url() -> str:
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url

    db_host = os.getenv("DB_HOST")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_port = os.getenv("DB_PORT", "5432")

    if db_host and db_name and db_user and db_password:
        return f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    sqlite_dir = BASE_DIR / "data"
    sqlite_dir.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{(sqlite_dir / 'app.db').as_posix()}"


def _build_engine(database_url: str) -> Engine:
    if database_url.startswith("sqlite"):
        return create_engine(database_url, connect_args={"check_same_thread": False})
    return create_engine(database_url, pool_pre_ping=True)


engine = _build_engine(_resolve_database_url())


def _initialize_database() -> None:
    last_error: SQLAlchemyError | None = None
    for _ in range(15):
        try:
            metadata.create_all(engine)
            return
        except SQLAlchemyError as error:
            last_error = error
            time.sleep(2)

    raise RuntimeError(f"Database initialization failed: {last_error}")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
def read_index(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "items": _list_items(),
        },
    )


@app.post("/items")
def create_item(title: str = Form(...), description: str = Form("")):
    _create_item(title=title.strip(), description=description.strip())

    return RedirectResponse(url="/", status_code=303)


@app.get("/items/{item_id}/edit")
def read_edit_item(request: Request, item_id: int):
    item = _get_item_or_404(item_id)
    return templates.TemplateResponse(request, "edit.html", {"item": item})


@app.post("/items/{item_id}/edit")
def update_item(item_id: int, title: str = Form(...), description: str = Form("")):
    _get_item_or_404(item_id)
    _update_item(item_id=item_id, title=title.strip(), description=description.strip())
    return RedirectResponse(url="/", status_code=303)


@app.post("/items/{item_id}/delete")
def delete_item(item_id: int):
    _delete_item(item_id)
    return RedirectResponse(url="/", status_code=303)


def _get_item_or_404(item_id: int) -> dict[str, str | int]:
    with engine.connect() as connection:
        row = connection.execute(
            select(items_table.c.id, items_table.c.title, items_table.c.description).where(items_table.c.id == item_id)
        ).mappings().first()

    if row:
        return dict(row)

    raise HTTPException(status_code=404, detail="Item not found")


def _list_items() -> list[dict[str, str | int]]:
    with engine.connect() as connection:
        rows = connection.execute(
            select(items_table.c.id, items_table.c.title, items_table.c.description).order_by(items_table.c.id)
        ).mappings().all()
    return [dict(row) for row in rows]


def _create_item(title: str, description: str) -> int:
    with engine.begin() as connection:
        result = connection.execute(insert(items_table).values(title=title, description=description))
        return int(result.inserted_primary_key[0])


def _update_item(item_id: int, title: str, description: str) -> None:
    with engine.begin() as connection:
        connection.execute(
            update(items_table).where(items_table.c.id == item_id).values(title=title, description=description)
        )


def _delete_item(item_id: int) -> None:
    with engine.begin() as connection:
        deleted = connection.execute(delete(items_table).where(items_table.c.id == item_id)).rowcount
        if not deleted:
            raise HTTPException(status_code=404, detail="Item not found")


def _reset_items_for_tests() -> None:
    _initialize_database()
    with engine.begin() as connection:
        connection.execute(delete(items_table))
