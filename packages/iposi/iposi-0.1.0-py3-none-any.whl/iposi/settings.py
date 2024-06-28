from typing import Optional

from pydantic import model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Settings provided as environment variables.

    IPOSI_HOST: Hostname of the SMTP server
    IPOSI_PASSWORD: Password for the SMTP server
    IPOSI_PORT: Port on which the SMTP server is listening
    IPOSI_USERNAME: Username for the SMTP server
    IPOSI_USE_TLS: Whether to use TLS

    IPOSI_PASSWORD and IPOSI_USERNAME require each other.
    """

    iposi_host: str
    iposi_password: Optional[str] = None
    iposi_port: int = 587
    iposi_username: Optional[str] = None
    iposi_use_tls: bool = True

    @model_validator(mode="after")
    def username_requires_password(self) -> "Settings":
        if self.iposi_username and not self.iposi_password:
            raise ValueError(
                "The environment variable IPOSI_PASSWORD must also be set "
                "if IPOSI_USERNAME is set."
            )
        return self

    @model_validator(mode="after")
    def password_requires_username(self) -> "Settings":
        if self.iposi_password and not self.iposi_username:
            raise ValueError(
                "The environment variable IPOSI_USERNAME must also be set "
                "if IPOSI_PASSWORD is set."
            )
        return self


def get_settings() -> Settings:
    """
    Return the configuration settings.
    """
    return Settings()  # type: ignore
