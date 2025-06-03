from django.contrib import admin
from .models import IntakeForm


@admin.register(IntakeForm)
class IntakeFormAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "phone",
        "scheduled_date",
        "submitted_at",
    )
    list_filter = (
        "submitted_at",
        "scheduled_date",
    )
    search_fields = (
        "name",
        "email",
        "phone",
        "message",
    )
    readonly_fields = ("submitted_at",)
    fieldsets = (
        ("Contact Info", {"fields": ("name", "email", "phone")}),
        ("Message", {"fields": ("message",)}),
        ("Scheduling", {"fields": ("scheduled_date",)}),
        ("System Info", {"fields": ("submitted_at",)}),
    )
    date_hierarchy = "submitted_at"
    ordering = ("-submitted_at",)
