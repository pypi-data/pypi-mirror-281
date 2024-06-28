from email_broadcasting.core._base import BaseMailBroadcaster


class MailBroadcasterSyncBase(BaseMailBroadcaster):
    def send_emails(
        self,
        recipients: list[str],
        subject: str = "test",
        body: str = "test",
        send_from: str = "control@corp-view.ru",
    ):
        return self._send_emails(
            recipients=recipients,
            subject=subject,
            body=body,
            send_from=send_from,
        )


class MailBroadcasterSyncSmtpSSL(MailBroadcasterSyncBase):
    pass
