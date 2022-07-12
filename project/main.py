from fastapi import FastAPI

import odoo

from odoo_fastapi.src.urls import router as src_router

app = FastAPI(title="Odoo-Fastapi")


@app.on_event("startup")
def set_default_executor() -> None:
    from concurrent.futures import ThreadPoolExecutor
    import asyncio

    loop = asyncio.get_running_loop()
    # Tune this according to your requirements !
    loop.set_default_executor(ThreadPoolExecutor(max_workers=5))


@app.on_event("startup")
def initialize_odoo() -> None:
    # Read Odoo config from $ODOO_RC.
    odoo.tools.config.parse_config([])





# register main router
app.include_router(src_router)
