from ninja import Router
from clients.tasks import send_email
from clients.models import IntakeForm
from clients.api.schema import IntakeFormSchema
from django.utils.dateparse import parse_datetime

router = Router()


@router.post("book-a-call", response=dict)
def book_a_call(request, data: IntakeFormSchema):
    scheduled_dt = parse_datetime(data.scheduled_date)

    intake = IntakeForm.objects.create(
        name=data.name,
        email=data.email,
        phone=data.phone,
        message=data.message,
        scheduled_date=scheduled_dt,
    )

    subject = f"New Call Scheduled by {intake.name}"
    message = f"""
Hello Admin,

A new call has been booked via the website.

Here are the details:

Name: {intake.name}
Email: {intake.email}
Phone: {intake.phone or 'N/A'}
Scheduled Date: {intake.scheduled_date.strftime('%B %d, %Y at %I:%M %p') if intake.scheduled_date else 'Not provided'}
Message: {intake.message}

This submission was received on: {intake.submitted_at.strftime('%B %d, %Y at %I:%M %p')}

Please reach out promptly.
"""

    send_email.delay(
        subject=subject,
        message=message,
        receiver_email_address="kitakayaloisa@gmail.com",
    )

    return {
        "success": True,
        "message": "Call has been scheduled and your form submitted.",
        "submission_id": intake.id,
    }
