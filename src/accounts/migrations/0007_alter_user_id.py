# Generated by Django 5.0.3 on 2024-03-28 17:18

import shortuuid.django_fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0006_user_id_alter_user_display_name_alter_user_status_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="id",
            field=shortuuid.django_fields.ShortUUIDField(
                alphabet=None,
                length=12,
                max_length=40,
                prefix="",
                primary_key=True,
                serialize=False,
            ),
        ),
    ]
