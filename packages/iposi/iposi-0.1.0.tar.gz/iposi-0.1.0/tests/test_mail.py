import os
import re
from smtplib import SMTPException, SMTPRecipientsRefused, SMTPResponseException

import pytest

from iposi import mail, MailError, MailFailure


def test_either_plain_text_or_html_required():
    with pytest.raises(ValueError, match="plain"):
        mail(
            sender="john@example.com",
            recipients="jane@example.org",
            subject="Some Test",
        )


def test_sending_fails(mock_smtp):
    # We test the following:
    # - A SMTPRecipientsRefused exception with a string as error is raised.
    # - A SMTPRecipientsRefused exception with a bytes array as error is raised.
    # - A SMTPResponseException exception with a string as error is raised.
    # - A SMTPResponseException exception with a bytes array as error is raised.
    # - A SMTPException is raised.
    # - No exception is raised.
    recipients = [
        "jane@example.org",
        "cecily@example.com",
        "peter@example.com",
        "ada@example.org",
        "doris@example.com",
        "bob@example.org",
    ]
    mock_smtp.return_value.__enter__.return_value.sendmail.side_effect = [
        SMTPRecipientsRefused(
            recipients={recipients[0]: (42, b"The answer was wrong")}
        ),
        SMTPRecipientsRefused(
            recipients={recipients[1]: (43, "The answer was still wrong")}
        ),
        SMTPResponseException(501, b"Bad recipient address"),
        SMTPResponseException(501, "Really bad recipient address"),
        SMTPException("What might the error be?"),
        {},  # is used as return value
    ]

    with pytest.raises(MailError) as exc_info:
        mail(
            sender="john@example.com",
            recipients=recipients,
            subject="Some Test",
            plain="Some text",
        )
    recipient_failures = exc_info.value.recipient_failures
    assert len(recipient_failures) == 5

    # first failure
    error = recipient_failures[recipients[0]]
    assert error.smtp_code == 42
    assert error.message == "The answer was wrong"
    assert error.smtp_exception is None

    # second failure
    error = recipient_failures[recipients[1]]
    assert error.smtp_code == 43
    assert error.message == "The answer was still wrong"
    assert error.smtp_exception is None

    # third failure
    error = recipient_failures[recipients[2]]
    assert error.smtp_code == 501
    assert error.message == "Bad recipient address"
    assert isinstance(error.smtp_exception, SMTPResponseException)

    # fourth failure
    error = recipient_failures[recipients[3]]
    assert error.smtp_code == 501
    assert error.message == "Really bad recipient address"
    assert isinstance(error.smtp_exception, SMTPResponseException)

    # fifth failure
    error = recipient_failures[recipients[4]]
    assert error.smtp_code is None
    assert error.message == "What might the error be?"
    assert isinstance(error.smtp_exception, SMTPException)


def test_sending_succeeds(mock_smtp):
    mock_smtp.return_value.__enter__.return_value.sendmail.return_value = {}

    mail(
        sender="john@example.com",
        recipients="jane@example.org",
        subject="Some Test",
        plain="Some text",
    )
    assert True


def test_configured_host_and_server_are_used(mock_smtp):
    os.environ["IPOSI_HOST"] = "some.host"
    os.environ["IPOSI_PORT"] = "42"

    mail(
        sender="john@example.com",
        recipients="jane@example.org",
        subject="Some Test",
        plain="Some text",
    )
    mock_smtp.assert_called_with(host="some.host", port=42)


def test_tls_used(mock_smtp):
    os.environ["IPOSI_USE_TLS"] = "1"
    mock_starttls = mock_smtp.return_value.__enter__.return_value.starttls

    mail(
        sender="john@example.com",
        recipients="jane@example.org",
        subject="Some Test",
        plain="Some text",
    )
    mock_starttls.assert_called_once()


def test_tls_not_used(mock_smtp):
    os.environ["IPOSI_USE_TLS"] = "0"
    mock_starttls = mock_smtp.return_value.__enter__.return_value.starttls

    mail(
        sender="john@example.com",
        recipients="jane@example.org",
        subject="Some Test",
        plain="Some text",
    )
    mock_starttls.assert_not_called()


def test_authentication_used(mock_smtp):
    os.environ["IPOSI_USERNAME"] = "admin"
    os.environ["IPOSI_PASSWORD"] = "not_very_secret"
    mock_login = mock_smtp.return_value.__enter__.return_value.login

    mail(
        sender="john@example.com",
        recipients="jane@example.org",
        subject="Some Test",
        plain="Some text",
    )
    mock_login.assert_called_with("admin", "not_very_secret")


def test_authentication_not_used(mock_smtp):
    del os.environ["IPOSI_USERNAME"]
    del os.environ["IPOSI_PASSWORD"]
    mock_login = mock_smtp.return_value.__enter__.return_value.login

    mail(
        sender="john@example.com",
        recipients="jane@example.org",
        subject="Some Test",
        plain="Some text",
    )
    mock_login.assert_not_called()


def test_email_is_sent_from_sender_to_single_recipient_with_subject(mock_smtp):
    mock_sendmail = mock_smtp.return_value.__enter__.return_value.sendmail

    mail(
        sender="john@example.com",
        recipients="jane@example.org",
        subject="Some Test",
        plain="Some text",
    )
    msg = mock_sendmail.call_args.kwargs["msg"]
    assert "From: john@example.com" in msg
    assert "To: jane@example.org" in msg
    assert "Subject: Some Test" in msg


def test_email_is_sent_from_sender_to_multiple_recipients_with_subject(mock_smtp):
    mock_sendmail = mock_smtp.return_value.__enter__.return_value.sendmail
    sender = "Ben Foster <foster@example.com>"
    recipients = ["Jerry Miller <jerry@example.org>", "Sarah Baker <sarah@example.org>"]

    mail(
        sender=sender,
        recipients=recipients,
        subject="Testing Recipients",
        plain="Some text",
    )
    assert len(mock_sendmail.call_args_list) == len(recipients)
    for index, call_args in enumerate(mock_sendmail.call_args_list):
        msg = call_args.kwargs["msg"]
        assert f"From: {sender}" in msg
        assert f"To: {recipients[index]}" in msg
        assert "Subject: Testing Recipients" in msg


def test_plain_text_and_html(mock_smtp):
    mock_sendmail = mock_smtp.return_value.__enter__.return_value.sendmail
    plain = "Some plain text content"
    html = "<p>Some HTML content</p>"

    mail(
        sender="john@example.com",
        recipients="jane@example.org",
        subject="Some Test",
        plain=plain,
        html=html,
    )
    msg = mock_sendmail.call_args.kwargs["msg"]
    content_pattern = (
        f"Content-Type: multipart/alternative.*"
        f"Content-Type: text/plain.*{plain}.*"
        f"Content-Type: text/html.*{html}"
    )
    assert re.search(content_pattern, msg, flags=re.DOTALL)


def test_plain_text_only(mock_smtp):
    mock_sendmail = mock_smtp.return_value.__enter__.return_value.sendmail
    plain = "Some plain text content"

    mail(
        sender="john@example.com",
        recipients="jane@example.org",
        subject="Some Test",
        plain=plain,
    )
    msg = mock_sendmail.call_args.kwargs["msg"]
    assert "text/html" not in msg
    content_pattern = (
        f"Content-Type: multipart/alternative.*Content-Type: text/plain.*{plain}"
    )
    assert re.search(content_pattern, msg, flags=re.DOTALL)


def test_html_only(mock_smtp):
    mock_sendmail = mock_smtp.return_value.__enter__.return_value.sendmail
    html = "<p>Some HTML content"

    mail(
        sender="john@example.com",
        recipients="jane@example.org",
        subject="Some Test",
        html=html,
    )
    msg = mock_sendmail.call_args.kwargs["msg"]
    assert "text/plain" not in msg
    content_pattern = (
        f"Content-Type: multipart/alternative.*Content-Type: text/html.*{html}"
    )
    assert re.search(content_pattern, msg, flags=re.DOTALL)


def test_mail_error_string_representation():
    mail_error = MailError(
        recipient_failures={
            "alice@example.org": MailFailure(
                smtp_code=None, message="Connection failed", smtp_exception=None
            ),
            "bob": MailFailure(
                smtp_code=501,
                message="Invalid address",
                smtp_exception=SMTPException("Something is wrong"),
            ),
        }
    )

    assert "alice@example.org" in str(mail_error)
    assert "Connection failed" in str(mail_error)
    assert "bob" in str(mail_error)
    assert "501" in str(mail_error)
    assert "Invalid address" in str(mail_error)
