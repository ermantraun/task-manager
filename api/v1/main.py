import config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from handlers import task
from dishka.integrations.fastapi import setup_dishka, FastapiProvider
from dishka import make_async_container
from ioc import FastApiApp
from config import Config
from handlers import exceptions_handlers

config = Config()

container = make_async_container(FastApiApp(), FastapiProvider(), context={Config: config})
def get_fastapi_app() -> FastAPI:

    app = FastAPI(title=config.fastapi.title, version=config.fastapi.version, description=config.fastapi.description)

    app.add_middleware(
    CORSMiddleware,
    allow_origins=config.fastapi.allow_origins,
    allow_credentials=config.fastapi.allow_credentials,
    allow_methods=config.fastapi.allow_methods,
    allow_headers=config.fastapi.allow_headers,
    )

    for exc_type, handler in exceptions_handlers.all_handlers.items():
        app.add_exception_handler(exc_type, handler)
    
    app.include_router(task.router)
    setup_dishka(container, app)
    return app

def get_app() -> FastAPI:
    return get_fastapi_app()

app = get_app()
