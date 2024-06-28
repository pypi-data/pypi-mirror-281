import smtplib


class SmtpSSLMixin:
    def smtp_instance(self, *args, **kwargs):
        return smtplib.SMTP_SSL(*args, **kwargs)
