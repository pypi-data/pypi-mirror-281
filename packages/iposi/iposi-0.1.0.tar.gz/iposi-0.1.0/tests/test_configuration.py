import os

import pytest
from pydantic_core._pydantic_core import ValidationError

from iposi import mail
from iposi.settings import get_settings


def _mail():
    mail(
        sender="John Doe <joe@example.com>",
        recipients="Jane Miller <jane@example.com>",
        subject="Test",
        plain="Some plain text content.",
        html="<html>Some HTML content.</html>",
    )


def test_all_settings_present(mock_smtp):
    _mail()


def test_host_is_required():
    del os.environ["IPOSI_HOST"]
    with pytest.raises(ValidationError):
        _mail()


def test_username_and_password_are_optional(mock_smtp):
    del os.environ["IPOSI_PASSWORD"]
    del os.environ["IPOSI_USERNAME"]
    _mail()


def test_username_requires_password():
    del os.environ["IPOSI_PASSWORD"]
    with pytest.raises(ValueError, match="must also be set"):
        _mail()


def test_password_requires_username():
    del os.environ["IPOSI_USERNAME"]
    with pytest.raises(ValueError, match="must also be set"):
        _mail()


def test_port_defaults_to_587():
    del os.environ["IPOSI_PORT"]
    settings = get_settings()
    assert settings.iposi_port == 587


def test_use_tls_defaults_to_true():
    del os.environ["IPOSI_USE_TLS"]
    settings = get_settings()
    assert settings.iposi_use_tls
