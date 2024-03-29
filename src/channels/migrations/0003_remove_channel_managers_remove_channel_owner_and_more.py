# Generated by Django 5.0.2 on 2024-03-10 19:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "channels",
            "0002_remove_channel_owners_channel_managers_channel_owner_and_more",
        ),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="channel",
            name="managers",
        ),
        migrations.RemoveField(
            model_name="channel",
            name="owner",
        ),
        migrations.RemoveField(
            model_name="channel",
            name="subscribers",
        ),
        migrations.AddField(
            model_name="channel",
            name="category",
            field=models.CharField(
                choices=[
                    ("NEWS", "News & Politics"),
                    ("EDU", "Education"),
                    ("ENT", "Entertainment"),
                    ("LIFE", "Lifestyle"),
                    ("TECH", "Technology & Science"),
                    ("GAME", "Gaming"),
                    ("MUS", "Music"),
                    ("VLOG", "Vlogging"),
                    ("SPRT", "Sports"),
                    ("TRVL", "Travel & Events"),
                    ("FOOD", "Food & Cooking"),
                    ("BF", "Beauty & Fashion"),
                    ("SCI", "Science"),
                    ("DIY", "DIY & Crafts"),
                    ("ANIM", "Animation"),
                    ("FA", "Film & Animation"),
                    ("KIDS", "Kids & Family"),
                    ("HW", "Health & Wellness"),
                ],
                default="ENT",
            ),
        ),
        migrations.AddField(
            model_name="channel",
            name="cover_picture_url",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="channel",
            name="creators",
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name="channel",
            name="profile_picture_url",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="channel",
            name="total_posts_count",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="channel",
            name="total_subscribers_count",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="channel",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="channel",
            name="name",
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.CreateModel(
            name="ChannelMember",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_owner", models.BooleanField()),
                (
                    "channel_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="channels.channel",
                    ),
                ),
                (
                    "uid",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Links",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("display_name", models.CharField(blank=True, null=True)),
                ("url", models.URLField()),
                (
                    "channel_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="channel_links",
                        to="channels.channel",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="channel",
            name="links",
            field=models.ManyToManyField(blank=True, to="channels.links"),
        ),
    ]
