from django.db import models
from accounts.models import User


class Link(models.Model):
    channel_id = models.ForeignKey("Channel", on_delete=models.CASCADE, related_name="channel_links")
    display_name = models.CharField(blank=True, null=True)
    url = models.URLField(max_length=200)


class ChannelMember(models.Model):
    channel_id = models.ForeignKey("Channel", on_delete=models.CASCADE, related_name="channel_members")
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    is_owner = models.BooleanField()

class Channel(models.Model):
    # TODO: Confirm with Paul and Antonio for Category set
    NEWS = 'NEWS'
    EDUCATION = 'EDU'
    ENTERTAINMENT = 'ENT'
    LIFESTYLE = 'LIFE'
    TECHNOLOGY = 'TECH'
    GAMING = 'GAME'
    MUSIC = 'MUS'
    VLOG = 'VLOG'
    SPORTS = 'SPRT'
    TRAVEL = 'TRVL'
    FOOD = 'FOOD'
    BEAUTY_FASHION = 'BF'
    SCIENCE = 'SCI'
    DIY = 'DIY'
    ANIMATION = 'ANIM'
    FILM_ANIMATION = 'FA'
    KIDS = 'KIDS'
    HEALTH_WELLNESS = 'HW'

    CATEGORY_CHOICES = [
        (NEWS, 'News & Politics'),
        (EDUCATION, 'Education'),
        (ENTERTAINMENT, 'Entertainment'),
        (LIFESTYLE, 'Lifestyle'),
        (TECHNOLOGY, 'Technology & Science'),
        (GAMING, 'Gaming'),
        (MUSIC, 'Music'),
        (VLOG, 'Vlogging'),
        (SPORTS, 'Sports'),
        (TRAVEL, 'Travel & Events'),
        (FOOD, 'Food & Cooking'),
        (BEAUTY_FASHION, 'Beauty & Fashion'),
        (SCIENCE, 'Science'),
        (DIY, 'DIY & Crafts'),
        (ANIMATION, 'Animation'),
        (FILM_ANIMATION, 'Film & Animation'),
        (KIDS, 'Kids & Family'),
        (HEALTH_WELLNESS, 'Health & Wellness'),
    ]

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, default=ENTERTAINMENT)
    creators = models.ManyToManyField(ChannelMember)
    total_subscribers_count = models.IntegerField(default=0)
    total_posts_count = models.IntegerField(default=0)
    profile_picture_url = models.URLField(max_length=200, blank=True, null=True)
    cover_picture_url = models.URLField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    links = models.ManyToManyField(Link, blank=True)
