import os, sys
import django
import traceback
sys.path.append("../")
os.environ['DJANGO_SETTINGS_MODULE'] = 'avrseauth.settings'
django.setup()

from datetime import datetime

from django.db.models import Q, Sum
from django.conf import settings
from django.contrib.humanize.templatetags.humanize import intcomma

from disco.bot import Plugin
from social_django.models import UserSocialAuth

from eveauth.discord.commands import BotCommands
from sde.models import System


class AuthPlugin(Plugin):
    # Public commands
    @Plugin.listen('MessageCreate')
    def public_commands(self, event):
        try:
            tokens = event.content.split()

            if tokens[0] == "!evetime":
                event.reply(datetime.utcnow().strftime("EVETime: %H:%M:%S"))

            elif tokens[0] == "!range":
                system = System.objects.filter(
                    name__istartswith=" ".join(tokens[1:])
                )
                if system.count() > 1:
                    event.reply(
                        "```Multiple Systems Found:\n%s```" % (
                            ", ".join(
                                map(
                                    lambda x: "%s (%s)" % (
                                        x.name,
                                        x.region.name
                                    ),
                                    system.all()
                                )
                            )
                        )
                    )
                elif system.count() == 1:
                    system = system.first()
                    event.reply(
                        "\n".join(
                            [
                                "http://evemaps.dotlan.net/range/Redeemer,5/%s" % system.name.replace(" ", "_"),
                                "http://evemaps.dotlan.net/range/Archon,5/%s" % system.name.replace(" ", "_"),
                                "http://evemaps.dotlan.net/range/Aeon,5/%s" % system.name.replace(" ", "_")
                            ]
                        )
                    )
        except:
            traceback.print_exc()

    # FC Tools
    @Plugin.listen('MessageCreate')
    def fc_commands(self, event):
        try:
            # Tokenise commands
            tokens = event.content.split()
            if tokens[0].startswith("!"):
                user = self._get_social(event.member.id).user
                commands = BotCommands(tokens, user, event)

                # Authenticated commands
                if tokens[0] == "!wallet":
                    wallet = user.characters.aggregate(Sum('wallet'))
                    event.reply(
                        "%s ISK" % (
                            intcomma(wallet['wallet__sum'])
                        )
                    )
                elif tokens[0].lower() == "!kills":
                    commands.kills()
                elif tokens[0].lower() == "!sabrefeed":
                    commands.sabrefeed()

                admin = user.groups.filter(name="FC").exists()
                hr = user.groups.filter(name="HR").exists()

                # Admin only commands
                if admin:
                    if tokens[0].lower() == "!fatigue":
                        commands.fatigue(admin=True)
                    elif tokens[0].lower() == "!alts":
                        commands.alts()
                    elif tokens[0].lower() == "!whoin":
                        commands.whoin()
                    elif tokens[0].lower() == "!whoinrange":
                        commands.whoinrange()
                    elif tokens[0].lower() == "!supers":
                        commands.supers()
                    elif tokens[0].lower() == "!sabres" or tokens[0].lower() == "!dictors":
                        commands.sabres()
                    elif tokens[0].lower() == "!strip":
                        commands.strip(admin=True)
                    elif tokens[0].lower() == "!jcs":
                        commands.jcs()
                    elif tokens[0].lower() == "!locate":
                        commands.locate(admin=True)
                    elif tokens[0].lower() == "!setmessage":
                        commands.setmessage()

                if hr:
                    if tokens[0].lower() == "!alts":
                        commands.alts()
                    elif tokens[0].lower() == "!locate":
                        commands.locate(admin=True)

                # public commands with limitations
                else:
                    if tokens[0].lower() == "!fatigue":
                        commands.fatigue(admin=False)
                    elif tokens[0].lower() == "!strip":
                        commands.strip(admin=False)
                    elif tokens[0].lower() == "!locate":
                        commands.locate(admin=False)
        except:
            traceback.print_exc()


    # Handle guild member joins
    @Plugin.listen('GuildMemberAdd')
    def guild_member_join(self, event):
        try:
            # Kick the user if they aren't authed
            social = self._get_social(event.member.id)
            if not social:
                if event.member.id not in settings.DISCORD_ALLOWED_BOTS:
                    return
                else:
                    event.member.kick()

            # Set their nickname to their EVE Character
            event.member.set_nickname(social.user.profile.character.name[:32])

            # Set corp role
            event.member.add_role(self._get_role(event.guild, social.user.profile.corporation.ticker))

            # Set regular group roles
            groups = social.user.groups.exclude(
                Q(name__startswith="Corp: ") | Q(name__startswith="Alliance: ")
            ).all()
            for group in groups:
                event.member.add_role(self._get_role(event.guild, group.name))

            # Set Access Level Group
            access_level = ["Non-member", "Blue", "Member"][social.user.profile.level]
            event.member.add_role(self._get_role(event.guild, access_level))
        except:
            traceback.print_exc()


    # Try to get the social object from a discord ID. Return None if not found
    def _get_social(self, uid):
        return UserSocialAuth.objects.filter(uid=uid).first()


    # Get a role object from a string
    def _get_role(self, guild, name):
        # Check if the role already exists
        for role in guild.roles.values():
            if role.name == name:
                return role

        # It doesn't so lets make it
        role = guild.create_role()
        self.client.api.guilds_roles_modify(guild.id, role.id, name=name)
        return role
