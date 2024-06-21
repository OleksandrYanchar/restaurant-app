import logging
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from .tokens import EmailTokenGenerator
from rest_framework.request import Request
from apps.accounts.models import User


def _send_verification_email(request: Request, user: User) -> None:
    subject = "Activate Your Account"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    try:
        current_site = get_current_site(request)
        body = render_to_string(
            "email_verification.html",
            {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": EmailTokenGenerator().make_token(user),
            },
        )
        send_mail(
            subject=subject,
            message="",
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=body,
            fail_silently=False,
        )
    except Exception as e:
        logging.error(f"Error sending email: {str(e)}")
        raise Exception(f"Error sending email: {str(e)}")


def _send_password_reset_email(request: Request, user: User) -> None:
    subject = "Passowrd Reset"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    try:
        current_site = get_current_site(request)
        body = render_to_string(
            "password-reset.html",
            {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": EmailTokenGenerator().make_token(user),
            },
        )
        send_mail(
            subject=subject,
            message="",
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=body,
            fail_silently=False,
        )
    except Exception as e:
        logging.error(f"Error sending email: {e}")
        raise Exception("Error sending email")
