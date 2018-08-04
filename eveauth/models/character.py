from datetime import datetime, timedelta

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from social_django.models import UserSocialAuth

from sde.models import System, Type, Station

from .corporation import Corporation
from .alliance import Alliance


class Character(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64)
    last_updated = models.DateTimeField(auto_now=True)

    # Extra details, these are default null
    token = models.ForeignKey(UserSocialAuth, null=True, default=None, on_delete=models.SET_NULL)
    owner = models.ForeignKey(User, null=True, default=None, related_name="characters", on_delete=models.SET_NULL)
    corp = models.ForeignKey(Corporation, null=True, default=None, related_name="characters", on_delete=models.SET_NULL)
    alliance = models.ForeignKey(Alliance, null=True, default=None, related_name="characters", on_delete=models.SET_NULL)

    wallet = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    system = models.ForeignKey(System, null=True, default=None, on_delete=models.SET_NULL)
    ship = models.ForeignKey(Type, null=True, default=None, on_delete=models.SET_NULL)
    home = models.ForeignKey(Station, null=True, default=None, related_name="characters", on_delete=models.SET_NULL)

    fatigue_expire_date = models.DateTimeField(null=True, default=None)
    last_jump_date = models.DateTimeField(null=True, default=None)
    clone_jump_ready = models.DateTimeField(null=True, default=None)

    last_login = models.DateTimeField(null=True, default=None)
    last_logoff = models.DateTimeField(null=True, default=None)

    visible_to = models.IntegerField(null=True, default=None)
    visible_until = models.DateTimeField(null=True, default=None)

    class Meta:
        ordering = ["name"]


    def __str__(self):
        return self.name


    def are_scopes_updated(self):
        if self.token != None:
            for scope in settings.SOCIAL_AUTH_CHARACTER_AUTH_SCOPE:
                if scope not in self.token.extra_data['scopes']:
                    return False
            return True

    def missing_scopes(self):
        missing = []
        if self.token != None:
            for scope in settings.SOCIAL_AUTH_CHARACTER_AUTH_SCOPE:
                if scope not in self.token.extra_data['scopes']:
                    missing.append(scope)
        return missing


    def fatigue(self):
        if self.fatigue_expire_date != None:
            return self.fatigue_expire_date - timezone.now()

    def has_fatigue(self):
        if self.fatigue_expire_date == None:
            return False
        fatigue = self.fatigue_expire_date - timezone.now()
        return fatigue.total_seconds() > 0

    def fatigue_text(self, nf=False):
        if self.has_fatigue():
            delta = self.fatigue()
            out = "%.2i:%.2i:%.2i" % (
                (delta.seconds / 60 / 60) % 24,
                (delta.seconds / 60) % 60,
                delta.seconds % 60
            )

            if delta.days > 0:
                out = "%sD %s" % (str(delta.days), out)

            return out
        else:
            if nf:
                return "NF"
            else:
                return "None"

    def jc_cooldown(self):
        if self.clone_jump_ready != None:
            return self.clone_jump_ready - timezone.now()

    def has_jc_cooldown(self):
        if self.clone_jump_ready == None:
            return False
        cooldown = self.clone_jump_ready - timezone.now()
        return cooldown.total_seconds() > 0

    def jc_cooldown_text(self):
        if self.has_jc_cooldown():
            delta = self.jc_cooldown()
            out = "%.2i:%.2i:%.2i" % (
                (delta.seconds / 60 / 60) % 24,
                (delta.seconds / 60) % 60,
                delta.seconds % 60
            )

            if delta.days > 0:
                out = "%sD %s" % (str(delta.days), out)

            return out
        else:
            return "Ready"



    @staticmethod
    def get_or_create(id):
        from eveauth.esi import ESI

        db_char = Character.objects.filter(id=id)
        if len(db_char) == 0:
            api = ESI()
            char = api.get("/v4/characters/%s/" % id)
            db_char = Character(
                id=id,
                name=char['name']
            )
            db_char.save()
        else:
            db_char = db_char[0]

        return db_char