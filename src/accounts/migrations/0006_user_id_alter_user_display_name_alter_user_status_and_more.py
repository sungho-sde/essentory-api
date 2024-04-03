# Generated by Django 5.0.3 on 2024-03-28 16:58

import shortuuid.django_fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0005_user_updated_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="id",
            field=shortuuid.django_fields.ShortUUIDField(
                alphabet=None,
                length=12,
                max_length=40,
                prefix="",
                null=True,
                serialize=False,
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="display_name",
            field=models.CharField(
                blank=True, max_length=20, verbose_name="display name"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="status",
            field=models.CharField(
                choices=[
                    ("Active", "Active"),
                    ("Inactive", "Inactive"),
                    ("Suspended", "Suspended"),
                ],
                default="Active",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="uid",
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(max_length=20, unique=True),
        ),
    ]