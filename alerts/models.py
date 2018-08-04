import requests
import json

from django.db import models
from django.conf import settings


def simple_message(message):
    return {
        "content": message
    }


class Webhook(models.Model):
    EVENT_CHOICES = (
        ('structure_reinforce', "Structure Reinforce"),
        ('structure_anchoring', 'Structure Anchor/Unanchor'),
        ("low_fuel_filtered", "Low Fuel (Filtered)"),
        ("low_fuel_all", "Low Fuel (All)"),
        ("structure_attacked", "Structured Attacked"),
        ("group_app", "New Group Application"),
        ("character_added", "Character Added"),
        ("character_deleted", "Character Deleted"),
        ("character_expired", "Character Expired"),
        ("character_joined", "Character Joined Corp"),
        ("character_left", "Character Left Corp")
    )
    NOTIFY_CHOICES = (
        ('', 'No'),
        ('@here', '@here'),
        ('@everyone', '@everyone')
    )

    event = models.CharField(max_length=64, db_index=True, choices=EVENT_CHOICES, verbose_name="Event")
    url = models.CharField(max_length=512, verbose_name="URL")
    notify = models.CharField(max_length=32, default="", blank=True, choices=NOTIFY_CHOICES, verbose_name="Notify")
    active = models.BooleanField(default=True, verbose_name="Active")


    @staticmethod
    def send(event, message):
        hooks = Webhook.objects.filter(event=event)
        if not hooks.exists():
            return False

        for hook in hooks.filter(active=True).all():
            requests.post(
                hook.url,
                json=message
            ).content

            if hook.notify != "":
                requests.post(
                    hook.url,
                    data={
                        "content": "%s ^" % hook.notify
                    }
                )
        return True
