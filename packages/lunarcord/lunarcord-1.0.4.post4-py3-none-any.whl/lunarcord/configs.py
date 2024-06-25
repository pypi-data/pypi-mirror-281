"""
An extension for setting and managing default values to be used by your lunarcord `Bot`.
This should always be created in a cog, otherwise it is uneffective - unless you use `Bot.userConfig` instead.
Below is a short example:

```
from lunarcord.configs import UserConfiguration as User

config = User(
    nickname = "Guest", # The user's bot nickname
    coins = 0, # The user's coins (eg for an economy bot)
    achievements = [], # A list of unlocked achievements
    # And anything else you can imagine of.
)
```
"""

from .__core__.types import UserConfiguration, Configuration as BaseConfiguration

def userConfig(data: dict):

    """Creates a new `UserConfiguration` by an already existing dict."""
    return UserConfiguration(**data)