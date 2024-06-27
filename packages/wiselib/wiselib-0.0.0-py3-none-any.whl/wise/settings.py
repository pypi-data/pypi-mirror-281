from pydantic import StrictStr, BaseModel
from pydantic.v1 import BaseSettings


class EnvSettings(BaseSettings):
    debug: bool
    secret_key: StrictStr
    service_name: StrictStr


class SentrySettings(BaseModel):
    enabled: bool = False
    dsn: str = ""
    environment: str = "production"
    sample_rate: float | int = 1.0


class KafkaSettings(BaseModel):
    bootstrap_servers: StrictStr
    security_protocol: StrictStr
    sasl_mechanism: StrictStr
    username: StrictStr
    password: StrictStr
    group_id: StrictStr


class PostgresSettings(BaseModel):
    name: StrictStr
    user: StrictStr
    password: StrictStr
    host: StrictStr
    port: int


class RedisSettings(BaseModel):
    host: StrictStr
    port: int
    db: int = 0


class CelerySettings(BaseModel):
    enabled: bool = True
    broker_url: StrictStr
    default_queue: StrictStr = ""


class PrometheusSettings(BaseModel):
    enabled: bool = True
    prefix: StrictStr
    multiproc_dir: StrictStr = "/tmp/multiproc-tmp"


class TracingSettings(BaseModel):
    url: StrictStr = ""
    enabled: bool = False
    service_name: StrictStr
