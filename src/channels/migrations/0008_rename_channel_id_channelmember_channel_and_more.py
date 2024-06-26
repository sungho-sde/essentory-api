# Generated by Django 5.0.3 on 2024-04-01 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("channels", "0007_channel_owner_channelmember_user"),
    ]

    operations = [
        migrations.RenameField(
            model_name="channelmember",
            old_name="channel_id",
            new_name="channel",
        ),
        migrations.RenameField(
            model_name="link",
            old_name="channel_id",
            new_name="channel",
        ),
        migrations.RemoveField(
            model_name="channel",
            name="creators",
        ),
        migrations.RemoveField(
            model_name="channel",
            name="links",
        ),
    ]
