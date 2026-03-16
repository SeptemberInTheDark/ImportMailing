from django.contrib import admin

from mailings.models import MailingMessage


@admin.register(MailingMessage)
class MailingMessageAdmin(admin.ModelAdmin):
    list_display = ("external_id", "user_id", "email", "subject", "created_at", "sent_at")
    search_fields = ("external_id", "user_id", "email", "subject")
    list_filter = ("sent_at", "created_at")

