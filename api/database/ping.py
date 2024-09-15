import asyncpg
from api.config import config as cfg


async def ping_postgres_server():
    try:
        conn = await asyncpg.connect(dsn=cfg.pgsql.dsn)
        await conn.execute('SELECT 1')
        cfg.app.logger.info("You successfully connected to Postgresql!")
        await conn.close()
    except Exception as e:
        cfg.app.logger.error(e)
