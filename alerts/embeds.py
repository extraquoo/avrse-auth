from eveauth.esi import ESI
from eveauth.models.character import Character

from sde.models import System, Type, Station


def structure_state(timer, structure):
    return {
        "username": "Structure Bot",
        "embeds": [
            {
                "type": "rich",
                "title": "%s (%s) %s" % (
                    timer.system.name,
                    timer.system.region.name,
                    {
                        "AN": "started Anchoring",
                        "AR": "Reinforced into Armor",
                        "ST": "Reinforced into Structure",
                        "UN": "started Unanchoring"
                    }[timer.stage]
                ),
                "description": "%s - %s (%s)" % (
                    timer.system.name,
                    timer.name,
                    timer.structure.name
                ),
                "thumbnail": {
                    "url": "https://imageserver.eveonline.com/Render/%s_128.png" % structure.type_id
                },
                "color": {
                    "AN": 0x0000ff,
                    "AR": 0xffff00,
                    "ST": 0xff0000,
                    "UN": 0x0000ff
                }[timer.stage],
                "fields": [
                    {
                        "name": "Timer",
                        "value": timer.date.strftime("%Y/%m/%d %H:%M"),
                        "inline": True,
                    },
                    {
                        "name": "Owner",
                        "value": "%s [%s]" % (
                            structure.corporation.name,
                            structure.corporation.ticker
                        ),
                        "inline": True,
                    }
                ]
            }
        ]
    }


def low_fuel(structure):
    return {
        "username": "Structure Bot",
        "embeds": [
            {
                "type": "rich",
                "title": "%s is low on fuel" % structure.type.name,
                "description": "%s (%s)" % (
                    structure.station.name,
                    structure.type.name
                ),
                "thumbnail": {
                    "url": "https://imageserver.eveonline.com/Render/%s_128.png" % structure.type_id
                },
                "color": 0x00ffff,
                "fields": [
                    {
                        "name": "Fuel Expires",
                        "value": structure.fuel_expires.strftime("%Y/%m/%d %H:%M"),
                        "inline": True,
                    },
                    {
                        "name": "Owner",
                        "value": "%s [%s]" % (
                            structure.corporation.name,
                            structure.corporation.ticker
                        ),
                        "inline": True,
                    }
                ]
            }
        ]
    }


def group_app(group_app):
    return {
        "username": "Auth Bot",
        "embeds": [
            {
                "type": "rich",
                "title": "%s applied to %s" % (
                    group_app.user.profile.character.name,
                    group_app.group.name
                ),
                "thumbnail": {
                    "url": "https://imageserver.eveonline.com/Character/%s_512.jpg" % (
                        group_app.user.profile.character.id
                    )
                }
            }
        ]
    }


def structure_attacked(notification, api=ESI()):
    data = notification.data
    system = System.objects.get(id=data['solarsystemID'])
    structure_type = Type.objects.get(id=data['structureShowInfoData'][1])
    structure = Station.get_or_create(data['structureID'], api)
    attacker = Character.get_or_create(data['charID'])

    out = {
        "username": "Structure Bot",
        "embeds": [
            {
                "type": "rich",
                "title": "%s in %s is under attack" % (
                    structure_type.name,
                    system.name,
                ),
                "description": "%s (%s)" % (
                    structure.name,
                    system.region.name
                ),
                "url": "https://zkillboard.com/character/%s/" % attacker.id,
                "thumbnail": {
                    "url": "https://imageserver.eveonline.com/Render/%s_128.png" % structure_type.id
                },
                "color": 0xff0000,
                "fields": [
                    {
                        "name": "Owner",
                        "value": structure.corp_structure.corporation.name,
                        "inline": True,
                    },
                    {
                        "name": "Time",
                        "value": data.date.strftime("%H:%M"),
                        "inline": True,
                    },
                    {
                        "name": "Attacker",
                        "value": attacker.name,
                        "inline": True,
                    },
                    {
                        "name": "Attacker Corp",
                        "value": data['corpName'],
                        "inline": True,
                    }
                ]
            }
        ]
    }

    if "allianceName" in data:
        out['embeds'][0]['fields'].append(
            {
                "name": "Attacker Alliance",
                "value": data['allianceName'],
                "inline": True,
            }
        )

    return out



def character_embed(user, character, message, color):
    fields = [
        {
            "name": "Corp",
            "value": "%s [%s]" % (character.corp.name, character.corp.ticker),
        }
    ]
    if character.alliance is not None:
        fields.append(
            {
                "name": "Alliance",
                "value": "%s [%s]" % (character.alliance.name, character.alliance.ticker),
            }
        )

    return {
        "username": "Auth Bot",
        "embeds": [
            {
                "type": "rich",
                "title": "%s %s %s" % (
                    user.profile.character.name,
                    message,
                    character.name
                ),
                "thumbnail": {
                    "url": "https://imageserver.eveonline.com/Character/%s_512.jpg" % (
                        character.id
                    )
                },
                "color": color,
                "fields": fields
            }
        ]
    }


def character_added(user, character):
    return character_embed(user, character, "added character", 0x0000ff)

def character_deleted(user, character):
    return character_embed(user, character, "disconnected character", 0xff0000)

def character_expired(user, character):
    return character_embed(user, character, "expired token for", 0xffff00)

def character_joined(character, corp):
    if character.owner is not None:
        owned_by = character.owner.profile.character.name
    else:
        owned_by = "Unknown"

    return {
        "username": "Auth Bot",
        "embeds": [
            {
                "type": "rich",
                "title": "%s joined %s" % (character.name, corp.name),
                "thumbnail": {
                    "url": "https://imageserver.eveonline.com/Character/%s_512.jpg" % character.id
                },
                "color": 0x0000ff,
                "fields": [
                    {
                        "name": "Owned By",
                        "value": owned_by,
                        "inline": True,
                    }
                ]
            }
        ]
    }

def character_left(character, corp):
    if character.owner is not None:
        owned_by = character.owner.profile.character.name
    else:
        owned_by = "Unknown"

    return {
        "username": "Auth Bot",
        "embeds": [
            {
                "type": "rich",
                "title": "%s left %s" % (character.name, corp.name),
                "thumbnail": {
                    "url": "https://imageserver.eveonline.com/Character/%s_512.jpg" % character.id
                },
                "color": 0xff0000,
                "fields": [
                    {
                        "name": "Owned By",
                        "value": owned_by,
                        "inline": True,
                    }
                ]
            }
        ]
    }


#"AN": 0x0000ff,
#"AR": 0xffff00,
#"ST": 0xff0000,
#"UN": 0x0000ff