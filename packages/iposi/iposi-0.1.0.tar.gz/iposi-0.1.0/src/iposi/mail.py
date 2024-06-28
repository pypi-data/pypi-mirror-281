import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import (
    SMTPException,
    SMTP,
    SMTPResponseException,
    SMTPRecipientsRefused,
)
from typing import NamedTuple, Optional, Sequence, Union, Dict

from iposi.settings import get_settings


class MailFailure(NamedTuple):
    """
    A failure which occurred while trying to send an email to a recipient.

    Parameters
    ----------
    smtp_code:
        The SMTP (error) code, if there is one.
    message:
        The error message.
    smtp_exception:
        The SMTP exception related to this error, if there is one.
    """

    smtp_code: Optional[int]
    message: str
    smtp_exception: Optional[SMTPException]


class MailError(Exception):
    """
    An error which occurred while trying to send an email.

    The error contains a property recipient_failures, which is a dictionary of recipient email
    addresses and corresponding MailFailure instances.

    Parameters
    ----------
    recipient_failures:
        A dictionary of recipient addresses and corresponding errors.
    """

    def __init__(self, recipient_failures: Dict[str, MailFailure]):
        self._recipient_failures = recipient_failures

    @property
    def recipient_failures(self) -> Dict[str, MailFailure]:
        return self._recipient_failures

    def __str__(self) -> str:
        return str(self.recipient_failures)


def mail(
    sender: str,
    recipients: Union[str, Sequence[str]],
    subject: str,
    plain: Optional[str] = None,
    html: Optional[str] = None,
) -> None:
    """
    Send an email.

    The email content can be provided as plain text or HTML or both. If neither plain
    text nor HTML content is provided, a ValueError is raised. Plain text or HTML is
    only included in the email if you provide it; no "auto-conversion" is attempted. A
    ValueError is raised if you provide neither plain text nor HTML.

    Some environment variables must be set for using this function; see the
    documentation for details.

    The sender and recipients can be specified as an email address or as a name
    followed by the email address in angular brackets (such as "John Doe
    <john@example.com>"). A string (for a single recipient) or a list of strings (for
    multiple recipients) may be passed as recipients.

    If you specify multiple recipients, the email is sent individually to each of the
    recipients, so that the To field of the email contains the address of the recipient
    only.

    The email is sent as a multipart message.

    Sending the email is attempted for all recipients, even if it has already failed
    for some of them. In case any of the attempts has failed, a MailError is raised.
    This exception contains a recipient_failures property, which is a dictionary. The
    keys of this dictionary are the recipient email addresses which failed, and the
    values are the corresponding MailFailure instances. Note this behaviour differs
    from that of the sendmail method of the standard SMTP class.

    This function is not intended for sending bulk emails. If you have more than a
    handful of recipients, you might consider using another solution.

    Parameters
    ----------
    sender:
        The sender, i.e. the email address for the email's From field.
    recipients:
        The recipients, i.e. the email addresses for the email's To field.
    subject:
        The content of the email's Subject field.
    plain:
        The email content as plain text.
    html:
        The email content as HTML.

    Raises
    ------
    MailError:
        If the email could not be sent for one or multiple recipients.

    """

    # Get the SMTP configuration
    # We do this first so that unit tests for the settings don't need to mock SMTP.
    settings = get_settings()

    # Check there is content to send
    if not plain and not html:
        raise ValueError("At least one of plain text or HTML must be provided.")

    # If a string is passed as recipients, convert it into a list
    if isinstance(recipients, str):
        recipients = [recipients]

    with smtplib.SMTP(host=settings.iposi_host, port=settings.iposi_port) as smtp:
        # Use TLS, if requested
        if settings.iposi_use_tls:
            smtp.starttls()

        # Login, if requested
        if settings.iposi_username and settings.iposi_password:
            smtp.login(settings.iposi_username, settings.iposi_password)

        # Send the mail to all recipients, one by one, collecting any errors along the
        # way
        recipient_failures: Dict[str, MailFailure] = {}
        for recipient in recipients:
            try:
                result = _send_single_mail(
                    sender=sender,
                    recipient=recipient,
                    subject=subject,
                    plain=plain,
                    html=html,
                    smtp=smtp,
                )
                # As we call the sendmail of the SMTP class with a single recipient,
                # we should never get a non-empty dictionary as result. However, we
                # nonetheless handle this case, in case a future change leads to calls
                # to sendmail with multiple recipients.
                for r, e in result.items():  # pragma: no cover
                    recipient_failures[r] = MailFailure(
                        smtp_code=e[0], message=str(e[1]), smtp_exception=None
                    )
            except SMTPRecipientsRefused as e:
                rec_smtp_code, rec_smtp_error = e.recipients[recipient]
                # A SMTPRecipientsRefused is essentially a container, so we don't
                # include it in our error
                rec_smtp_error_as_str = (
                    rec_smtp_error.decode()
                    if isinstance(rec_smtp_error, bytes)
                    else rec_smtp_error
                )
                recipient_failures[recipient] = MailFailure(
                    rec_smtp_code, rec_smtp_error_as_str, None
                )
            except SMTPResponseException as e:
                res_smtp_code = e.smtp_code
                res_smtp_error = e.smtp_error
                res_smtp_error_as_str = (
                    res_smtp_error.decode()
                    if isinstance(res_smtp_error, bytes)
                    else res_smtp_error
                )
                recipient_failures[recipient] = MailFailure(
                    res_smtp_code, res_smtp_error_as_str, e
                )
            except SMTPException as e:
                recipient_failures[recipient] = MailFailure(None, str(e), e)

        if len(recipient_failures) > 0:
            raise MailError(recipient_failures=recipient_failures)


def _send_single_mail(
    sender: str,
    recipient: str,
    subject: str,
    plain: Optional[str],
    html: Optional[str],
    smtp: SMTP,
) -> dict[str, tuple[int, bytes]]:
    # Construct the email
    message = MIMEMultipart("alternative")
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    if plain:
        message.attach(MIMEText(plain))
    if html:
        message.attach(MIMEText(html, "html"))

    # Send the email
    return smtp.sendmail(
        from_addr=sender, to_addrs=[recipient], msg=message.as_string()
    )
