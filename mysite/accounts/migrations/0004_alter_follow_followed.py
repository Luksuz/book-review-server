# Generated by Django 4.2.7 on 2023-11-19 06:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0003_alter_customuser_password"),
    ]

    operations = [
        migrations.AlterField(
            model_name="follow",
            name="followed",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="followed",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
