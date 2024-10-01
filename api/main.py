import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse

from api import routes

root = os.path.dirname(os.path.abspath(__file__))
origins = ["*"]

app = FastAPI(
    title="Black Desert Boss API",
    description="API for Black Desert Boss",
    version="1.0.0",
    license_info={"name": "Apache 2.0", "url": "https://www.apache.org/licenses/LICENSE-2.0.html"},
    contact={
        "name": "SunTrack",
        "url": "https://t.me/suntrackspb",
    },
    terms_of_service="https://www.pearlcdn.com/ru/terms",
    docs_url=None,
    redoc_url='/api/redoc',
    openapi_url='/api/openapi.json'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/docs", include_in_schema=False)
def overridden_swagger() -> HTMLResponse:
    return get_swagger_ui_html(
        openapi_url="/api/openapi.json",
        title="Black Desert Boss API",
        swagger_favicon_url="https://s1.pearlcdn.com/RU/contents/img/common/favicon32_bdo.ico"
    )


app.include_router(
    routes.user_router,
    prefix="/api",
    tags=["Users"],
)

app.include_router(
    routes.boss_router,
    prefix="/api",
    tags=["Bosses"],
)

app.include_router(
    routes.notify_router,
    prefix="/api",
    tags=["Notifications"],
)

app.include_router(
    routes.promo_code_router,
    prefix="/api",
    tags=["Promo Codes"],
)


@app.get("/", tags=["Root"])
@app.get("/api", tags=["Root"])
async def read_root() -> HTMLResponse:
    return HTMLResponse(
        status_code=404,
        content="<center><h1>404 Not Found</h1></center><hr><center>nginx/1.18.0 (Ubuntu)</center>"
    )
