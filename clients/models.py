from django.db import models


class IntakeForm(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Full Name",
        help_text="The full name of the person submitting the form.",
    )
    email = models.EmailField(
        verbose_name="Email Address",
        help_text="The email address where the user can be contacted.",
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Phone Number",
        help_text="Optional phone number provided by the user.",
    )
    message = models.TextField(
        verbose_name="Message",
        help_text="The user's message or reason for scheduling a call.",
    )
    scheduled_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Scheduled Date and Time",
        help_text="Optional: the datetime selected by the user for a scheduled call.",
    )
    submitted_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Submitted At",
        help_text="The date and time the form was submitted.",
    )

    class Meta:
        verbose_name = "Intake Form Submission"
        verbose_name_plural = "Intake Form Submissions"
        ordering = ["-submitted_at"]
        get_latest_by = "submitted_at"

    def __str__(self):
        return f"{self.name} ({self.email}) - Submitted on {self.submitted_at.strftime('%Y-%m-%d %H:%M')}"
