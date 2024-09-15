import asyncio

import uvicorn
from api.config import config as cfg
from api.database.ping import ping_postgres_server

if __name__ == '__main__':
    asyncio.run(ping_postgres_server())

    uvicorn.run(
        app="api.main:app",
        host=cfg.app.host,
        port=cfg.app.port,
        log_config="logging_config.json"
    )
