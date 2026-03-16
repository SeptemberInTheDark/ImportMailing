from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MailingMessage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "external_id",
                    models.CharField(
                        max_length=255,
                        unique=True,
                        validators=[django.core.validators.MinLengthValidator(1)],
                        verbose_name="Внешний идентификатор",
                    ),
                ),
                ("user_id", models.CharField(max_length=255, verbose_name="Идентификатор пользователя")),
                ("email", models.EmailField(max_length=254, verbose_name="Email получателя")),
                ("subject", models.CharField(max_length=255, verbose_name="Тема письма")),
                ("message", models.TextField(verbose_name="Текст письма")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создано")),
                ("sent_at", models.DateTimeField(blank=True, null=True, verbose_name="Отправлено")),
            ],
            options={
                "verbose_name": "Письмо рассылки",
                "verbose_name_plural": "Письма рассылки",
            },
        ),
        migrations.AddIndex(
            model_name="mailingmessage",
            index=models.Index(fields=["external_id"], name="mailings_ma_externa_40ff77_idx"),
        ),
    ]

