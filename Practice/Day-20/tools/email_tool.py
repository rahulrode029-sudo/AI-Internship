from datetime import datetime


def send_email(
    recipient: str,
    subject: str,
    message: str
) -> str:
    """
    Simulate sending an email.

    Args:
        recipient: Email address.
        subject: Email subject.
        message: Email body.

    Returns:
        Email status.
    """

    try:
        if not recipient.strip():
            return "Email error: Recipient is required."

        if "@" not in recipient:
            return "Email error: Invalid email address."

        if not subject.strip():
            return "Email error: Subject is required."

        if not message.strip():
            return "Email error: Message is required."

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        return (
            "Email prepared successfully.\n"
            f"Recipient: {recipient}\n"
            f"Subject: {subject}\n"
            f"Message: {message}\n"
            f"Timestamp: {timestamp}\n"
            "Status: SIMULATED - email was not actually sent."
        )

    except Exception as e:
        return f"Email error: {e}"