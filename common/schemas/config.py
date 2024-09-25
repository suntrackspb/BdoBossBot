from dataclasses import dataclass
from logging import Logger


@dataclass
class AppConfig:
    host: str | None = None
    port: int | None = None
    secret: str | None = None
    logger: Logger | None = None


@dataclass
class TelegramConfig:
    bot_token: str | None = None
    web_api_url: int | None = None
    web_api_key: str | None = None


@dataclass
class PostgresCfg:
    name: str | None = None
    user: str | None = None
    password: str | None = None
    port: int | None = None
    host: str | None = None

    echo: bool = False

    def __post_init__(self):
        url = f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
        dsn = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
        self.url = url
        self.dsn = dsn


@dataclass
class ProxyConfig:
    ENABLED: bool
    PROXY_TYPE: str
    PROXY_HOST: str
    PROXY_PORT: int
    PROXY_LOGIN: str
    PROXY_PASSWORD: str

    def __post_init__(self):
        self.URL = f"{self.PROXY_TYPE}://{self.PROXY_LOGIN}:{self.PROXY_PASSWORD}@{self.PROXY_HOST}:{self.PROXY_PORT}"


@dataclass
class Config:
    app: AppConfig
    pgsql: PostgresCfg
    tlg: TelegramConfig
    proxy: ProxyConfig
