CREATE_INSTANT_INVITE = 1 << 0
KICK_MEMBERS = 1 << 1
BAN_MEMBERS = 1 << 2
ADMINISTRATOR = 1 << 3
MANAGE_CHANNELS = 1 << 4
MANAGE_GUILD = 1 << 5
ADD_REACTIONS = 1 << 6
VIEW_AUDIT_LOG = 1 << 7
PRIORITY_SPEAKER = 1 << 8
STREAM = 1 << 9
VIEW_CHANNEL = 1 << 10
SEND_MESSAGES = 1 << 11
SEND_TTS_MESSAGES = 1 << 12
MANAGE_MESSAGES = 1 << 13
EMBED_LINKS = 1 << 14
ATTACH_FILES = 1 << 15
READ_MESSAGE_HISTORY = 1 << 16
MENTION_EVERYONE = 1 << 17
USE_EXTERNAL_EMOJIS = 1 << 18
VIEW_GUILD_INSIGHTS = 1 << 19
CONNECT = 1 << 20
SPEAK = 1 << 21
MUTE_MEMBERS = 1 << 22
DEAFEN_MEMBERS = 1 << 23
MOVE_MEMBERS = 1 << 24
USE_VAD = 1 << 25
CHANGE_NICKNAME = 1 << 26
MANAGE_NICKNAMES = 1 << 27
MANAGE_ROLES = 1 << 28
MANAGE_WEBHOOKS = 1 << 29
MANAGE_EMOJIS_AND_STICKERS = 1 << 30
USE_APPLICATION_COMMANDS = 1 << 31
REQUEST_TO_SPEAK = 1 << 32
MANAGE_THREADS = 1 << 34
USE_PUBLIC_THREADS = 1 << 35
USE_PRIVATE_THREADS = 1 << 36
USE_EXTERNAL_STICKERS = 1 << 37

class Permissions:

    __slots__ = ("_all")

    def __init__(self):

        self._all: list[Permission] = []

    @property
    def all(self):
        """Returns a `list` of `Permission` objects, no matter whether they are allowed or denied."""
        return self._all
    
    @property
    def allowed(self):
        """Returns a `list` of allowed `Permissions` only."""
        return [x for x in self.all if x.allowed]
    
    @property
    def denied(self):
        """Returns a `list` of denied `Permissions` only."""
        return [x for x in self.all if x.denied]
    
    @property
    def value(self):
        """Returns the integer value for all the permissions."""

    @value.setter
    def value(self, new: int):

        for perm in self._all:
            perm.allowed = (new & perm.id) == perm.id
    
    def hasPermission(self, name: str):

        """Checks if the given permission is allowed for this object."""
        
        name = name.upper()

        for perm in self._all:
            if perm.name.upper() == name:
                return True
            
    def allowPermission(self, name: str, allow: bool = True):

        """Sets the given permission to `allowed`."""

        try:
            allow = bool(allow)
        except:
            return

        name = name.upper()

        for perm in self._all:
            if perm.name.upper() == name:
                perm.allowed = allow

    def denyPermission(self, name: str):
        """Sets the given permission to `denied`."""
        self.allowPermission(name, allow=False)

    def allowPermissions(self, *names: str):

        """Bulk-allow multiple permissions at once."""

        for name in names:
            self.allowPermission(name)

    def denyPermissions(self, *names: str):

        """Bulk-deny multiple permissions at once."""

        for name in names:
            self.denyPermission(name)

    @property
    def createInstantInvite(self):
        return self.hasPermission("CREATE_INSTANT_INVITE")

    @createInstantInvite.setter
    def createInstantInvite(self, new: bool):
        self.allowPermission("CREATE_INSTANT_INVITE", new)

    @property
    def kickMembers(self):
        return self.hasPermission("KICK_MEMBERS")

    @kickMembers.setter
    def kickMembers(self, new: bool):
        self.allowPermission("KICK_MEMBERS", new)

    @property
    def banMembers(self):
        return self.hasPermission("BAN_MEMBERS")

    @banMembers.setter
    def banMembers(self, new: bool):
        self.allowPermission("BAN_MEMBERS", new)

    @property
    def administrator(self):
        return self.hasPermission("ADMINISTRATOR")

    @administrator.setter
    def administrator(self, new: bool):
        self.allowPermission("ADMINISTRATOR", new)

    @property
    def manageChannels(self):
        return self.hasPermission("MANAGE_CHANNELS")

    @manageChannels.setter
    def manageChannels(self, new: bool):
        self.allowPermission("MANAGE_CHANNELS", new)

    @property
    def manageGuild(self):
        return self.hasPermission("MANAGE_GUILD")

    @manageGuild.setter
    def manageGuild(self, new: bool):
        self.allowPermission("MANAGE_GUILD", new)

    @property
    def addReactions(self):
        return self.hasPermission("ADD_REACTIONS")

    @addReactions.setter
    def addReactions(self, new: bool):
        self.allowPermission("ADD_REACTIONS", new)

    @property
    def viewAuditLog(self):
        return self.hasPermission("VIEW_AUDIT_LOG")

    @viewAuditLog.setter
    def viewAuditLog(self, new: bool):
        self.allowPermission("VIEW_AUDIT_LOG", new)

    @property
    def prioritySpeaker(self):
        return self.hasPermission("PRIORITY_SPEAKER")

    @prioritySpeaker.setter
    def prioritySpeaker(self, new: bool):
        self.allowPermission("PRIORITY_SPEAKER", new)

    @property
    def stream(self):
        return self.hasPermission("STREAM")

    @stream.setter
    def stream(self, new: bool):
        self.allowPermission("STREAM", new)

    @property
    def viewChannel(self):
        return self.hasPermission("VIEW_CHANNEL")

    @viewChannel.setter
    def viewChannel(self, new: bool):
        self.allowPermission("VIEW_CHANNEL", new)

    @property
    def sendMessages(self):
        return self.hasPermission("SEND_MESSAGES")

    @sendMessages.setter
    def sendMessages(self, new: bool):
        self.allowPermission("SEND_MESSAGES", new)

    @property
    def sendTtsMessages(self):
        return self.hasPermission("SEND_TTS_MESSAGES")

    @sendTtsMessages.setter
    def sendTtsMessages(self, new: bool):
        self.allowPermission("SEND_TTS_MESSAGES", new)

    @property
    def manageMessages(self):
        return self.hasPermission("MANAGE_MESSAGES")

    @manageMessages.setter
    def manageMessages(self, new: bool):
        self.allowPermission("MANAGE_MESSAGES", new)

    @property
    def embedLinks(self):
        return self.hasPermission("EMBED_LINKS")

    @embedLinks.setter
    def embedLinks(self, new: bool):
        self.allowPermission("EMBED_LINKS", new)

    @property
    def attachFiles(self):
        return self.hasPermission("ATTACH_FILES")

    @attachFiles.setter
    def attachFiles(self, new: bool):
        self.allowPermission("ATTACH_FILES", new)

    @property
    def readMessageHistory(self):
        return self.hasPermission("READ_MESSAGE_HISTORY")

    @readMessageHistory.setter
    def readMessageHistory(self, new: bool):
        self.allowPermission("READ_MESSAGE_HISTORY", new)

    @property
    def mentionEveryone(self):
        return self.hasPermission("MENTION_EVERYONE")

    @mentionEveryone.setter
    def mentionEveryone(self, new: bool):
        self.allowPermission("MENTION_EVERYONE", new)

    @property
    def useExternalEmojis(self):
        return self.hasPermission("USE_EXTERNAL_EMOJIS")

    @useExternalEmojis.setter
    def useExternalEmojis(self, new: bool):
        self.allowPermission("USE_EXTERNAL_EMOJIS", new)

    @property
    def viewGuildInsights(self):
        return self.hasPermission("VIEW_GUILD_INSIGHTS")

    @viewGuildInsights.setter
    def viewGuildInsights(self, new: bool):
        self.allowPermission("VIEW_GUILD_INSIGHTS", new)

    @property
    def connect(self):
        return self.hasPermission("CONNECT")

    @connect.setter
    def connect(self, new: bool):
        self.allowPermission("CONNECT", new)

    @property
    def speak(self):
        return self.hasPermission("SPEAK")

    @speak.setter
    def speak(self, new: bool):
        self.allowPermission("SPEAK", new)

    @property
    def muteMembers(self):
        return self.hasPermission("MUTE_MEMBERS")

    @muteMembers.setter
    def muteMembers(self, new: bool):
        self.allowPermission("MUTE_MEMBERS", new)

    @property
    def deafenMembers(self):
        return self.hasPermission("DEAFEN_MEMBERS")

    @deafenMembers.setter
    def deafenMembers(self, new: bool):
        self.allowPermission("DEAFEN_MEMBERS", new)

    @property
    def moveMembers(self):
        return self.hasPermission("MOVE_MEMBERS")

    @moveMembers.setter
    def moveMembers(self, new: bool):
        self.allowPermission("MOVE_MEMBERS", new)

    @property
    def useVad(self):
        return self.hasPermission("USE_VAD")

    @useVad.setter
    def useVad(self, new: bool):
        self.allowPermission("USE_VAD", new)

    @property
    def changeNickname(self):
        return self.hasPermission("CHANGE_NICKNAME")

    @changeNickname.setter
    def changeNickname(self, new: bool):
        self.allowPermission("CHANGE_NICKNAME", new)

    @property
    def manageNicknames(self):
        return self.hasPermission("MANAGE_NICKNAMES")

    @manageNicknames.setter
    def manageNicknames(self, new: bool):
        self.allowPermission("MANAGE_NICKNAMES", new)

    @property
    def manageRoles(self):
        return self.hasPermission("MANAGE_ROLES")

    @manageRoles.setter
    def manageRoles(self, new: bool):
        self.allowPermission("MANAGE_ROLES", new)

    @property
    def manageWebhooks(self):
        return self.hasPermission("MANAGE_WEBHOOKS")

    @manageWebhooks.setter
    def manageWebhooks(self, new: bool):
        self.allowPermission("MANAGE_WEBHOOKS", new)

    @property
    def manageEmojisAndStickers(self):
        return self.hasPermission("MANAGE_EMOJIS_AND_STICKERS")

    @manageEmojisAndStickers.setter
    def manageEmojisAndStickers(self, new: bool):
        self.allowPermission("MANAGE_EMOJIS_AND_STICKERS", new)

    @property
    def useApplicationCommands(self):
        return self.hasPermission("USE_APPLICATION_COMMANDS")

    @useApplicationCommands.setter
    def useApplicationCommands(self, new: bool):
        self.allowPermission("USE_APPLICATION_COMMANDS", new)

    @property
    def requestToSpeak(self):
        return self.hasPermission("REQUEST_TO_SPEAK")

    @requestToSpeak.setter
    def requestToSpeak(self, new: bool):
        self.allowPermission("REQUEST_TO_SPEAK", new)

    @property
    def manageEvents(self):
        return self.hasPermission("MANAGE_EVENTS")

    @manageEvents.setter
    def manageEvents(self, new: bool):
        self.allowPermission("MANAGE_EVENTS", new)

    @property
    def manageThreads(self):
        return self.hasPermission("MANAGE_THREADS")

    @manageThreads.setter
    def manageThreads(self, new: bool):
        self.allowPermission("MANAGE_THREADS", new)

    @property
    def createPublicThreads(self):
        return self.hasPermission("CREATE_PUBLIC_THREADS")

    @createPublicThreads.setter
    def createPublicThreads(self, new: bool):
        self.allowPermission("CREATE_PUBLIC_THREADS", new)

    @property
    def createPrivateThreads(self):
        return self.hasPermission("CREATE_PRIVATE_THREADS")

    @createPrivateThreads.setter
    def createPrivateThreads(self, new: bool):
        self.allowPermission("CREATE_PRIVATE_THREADS", new)

    @property
    def useExternalStickers(self):
        return self.hasPermission("USE_EXTERNAL_STICKERS")

    @useExternalStickers.setter
    def useExternalStickers(self, new: bool):
        self.allowPermission("USE_EXTERNAL_STICKERS", new)

    @property
    def sendMessagesInThreads(self):
        return self.hasPermission("SEND_MESSAGES_IN_THREADS")

    @sendMessagesInThreads.setter
    def sendMessagesInThreads(self, new: bool):
        self.allowPermission("SEND_MESSAGES_IN_THREADS", new)

    @property
    def useEmbeddedActivities(self):
        return self.hasPermission("USE_EMBEDDED_ACTIVITIES")

    @useEmbeddedActivities.setter
    def useEmbeddedActivities(self, new: bool):
        self.allowPermission("USE_EMBEDDED_ACTIVITIES", new)

    @property
    def moderateMembers(self):
        return self.hasPermission("MODERATE_MEMBERS")

    @moderateMembers.setter
    def moderateMembers(self, new: bool):
        self.allowPermission("MODERATE_MEMBERS", new)
            
    def __iter__(self):
        return self.allowed.__iter__()
    
    def __len__(self):
        return self.allowed.__len__()
    
    def __repr__(self):
        return f"<Permissions allowed={len(self.allowed)} denied={len(self.denied)} all={len(self.all)}>"

class Permission:

    __slots__ = ("name", "id", "value", "allowed")

    def __init__(self, perms: Permissions, name: str):

        self.name: str = name
        self.id: int = len(perms.all)
        self.value = 1 << self.id
        self.allowed: bool = False
        perms._all.append(self)

    @property
    def denied(self):
        return not self.allowed
    
    @denied.setter
    def denied(self, new: bool):
        self.allowed = not new

    def __repr__(self):
        return f"<Permission name=\"{self.name}\" id={self.id} allowed={self.allowed}"

ALL = [
    "CREATE_INSTANT_INVITE",
    "KICK_MEMBERS",
    "BAN_MEMBERS",
    "ADMINISTRATOR",
    "MANAGE_CHANNELS",
    "MANAGE_GUILD",
    "ADD_REACTIONS",
    "VIEW_AUDIT_LOG",
    "PRIORITY_SPEAKER",
    "STREAM",
    "VIEW_CHANNEL",
    "SEND_MESSAGES",
    "SEND_TTS_MESSAGES",
    "MANAGE_MESSAGES",
    "EMBED_LINKS",
    "ATTACH_FILES",
    "READ_MESSAGE_HISTORY",
    "MENTION_EVERYONE",
    "USE_EXTERNAL_EMOJIS",
    "VIEW_GUILD_INSIGHTS",
    "CONNECT",
    "SPEAK",
    "MUTE_MEMBERS",
    "DEAFEN_MEMBERS",
    "MOVE_MEMBERS",
    "USE_VAD",
    "CHANGE_NICKNAME",
    "MANAGE_NICKNAMES",
    "MANAGE_ROLES",
    "MANAGE_WEBHOOKS",
    "MANAGE_EMOJIS_AND_STICKERS",
    "USE_APPLICATION_COMMANDS",
    "REQUEST_TO_SPEAK",
    "MANAGE_EVENTS",
    "MANAGE_THREADS",
    "CREATE_PUBLIC_THREADS",
    "CREATE_PRIVATE_THREADS",
    "USE_EXTERNAL_STICKERS",
    "SEND_MESSAGES_IN_THREADS",
    "USE_EMBEDDED_ACTIVITIES",
    "MODERATE_MEMBERS"
]

def createPermissions():

    perms = Permissions()

    for x in ALL:

        Permission(
            perms=perms,
            name=x
        )

    return perms

def calculatePermissions(value: int):

    perms = createPermissions()
    perms.value = int(value)
    return perms