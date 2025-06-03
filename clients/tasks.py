import requests
from celery import shared_task
from django.conf import settings
from ninja.errors import HttpError
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.template.loader import render_to_string

def check_if_is_staff(user: User):
    if not user.is_staff:
        raise HttpError(401, "Unauthorized")


def check_if_is_active(email: str):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        raise HttpError(401, "User does not exist")
    if not user.is_active:
        raise HttpError(401, "Inactive account. Contact administrator.")


def get_client_ip(request):
    LOCAL_IP_PREFIXES = (
        "127.",  # Localhost IP (IPv4)
        "10.",  # Private network range 10.0.0.0 - 10.255.255.255
        "192.168.",  # Private network range 192.168.0.0 - 192.168.255.255
        "172.",  # Private network range 172.16.0.0 - 172.31.255.255
    )

    try:
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[-1].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")

        if ip == "localhost" or any(
            ip.startswith(prefix) for prefix in LOCAL_IP_PREFIXES
        ):
            raise Exception("Local IP address detected. Cannot determine external IP.")

        return ip
    except Exception as e:
        raise Exception(str(e))


TEMPLATE_CODE_NAME_MAP = {
    "PR": "temps/password_reset.html",
    "MWE": "temps/manager_welcome_email.html",
    "TWE": "temps/tenant_welcome_email.html",
    "AV": "temps/account_verification.html",
    "LB": "temps/lease_billing.html",
    "PC": "temps/payment_confirmation.html",
    "GN": "temps/general_notification.html",
    "MMR": "temps/manager_maintenance_request.html",
    "TMR": "temps/tenant_maintenance_request.html",
    "MLD": "temps/manager_lease_document.html",
    "TLD": "temps/tenant_lease_document.html",
}


def find_template(template_code_name: str) -> str:
    try:
        template = TEMPLATE_CODE_NAME_MAP.get(template_code_name)

        if not template:
            raise Exception(f"Unknown template code: {template_code_name}.")

        return template
    except Exception as e:
        raise Exception(str(e))

@shared_task
def send_email(
    subject: str,
    receiver_email_address: str,
    sender_email_address: str = settings.EMAIL_HOST_USER,
    **kwargs,
):
    mail_data = kwargs.get("mail_data", None)

    template_code_name = kwargs.get("template_code_name", None)

    if template_code_name and mail_data:
        template = find_template(str(template_code_name))

        html_content = render_to_string(template_name=template, context=dict(mail_data))

        plain_content = strip_tags(html_content)

        send_mail(
            subject=subject,
            message=plain_content,
            from_email=sender_email_address,
            recipient_list=[
                receiver_email_address,
            ],
            html_message=html_content,
            fail_silently=True,
        )

    send_mail(
        subject=subject,
        message=str(kwargs.get("message")),
        from_email=sender_email_address,
        recipient_list=[
            receiver_email_address,
        ],
        fail_silently=True,
    )


def create_notification(recipient_id: str, message: str, url_path: str):
    try:
        payload = {
            "recipient_id": recipient_id,
            "message": message,
            "url_path": url_path,
        }

        base_url = settings.TALKS_URL

        url = f"{base_url}/notifications/webhook"

        try:
            res = requests.post(url, json=payload, timeout=5)

            if res.status_code != 200 or res.json().get("status") != "success":
                raise Exception(
                    f"Failed to create notification. Status code: {res.status_code}."
                )

            return True
        except Exception as e:
            raise Exception(str(e))
    except Exception as e:
        raise Exception(str(e))
