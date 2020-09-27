import random
import typing
from pathlib import Path

import csv
import discord

FILE_DIR = Path(__file__).resolve().parent
SECRETS_DIR = FILE_DIR / "secrets"

Emoji = typing.Union[discord.Emoji, str]
import functools


@functools.lru_cache
def global_emoji() -> typing.Dict[str, str]:
    with open(FILE_DIR / "emoji.csv") as emoji_file:
        emoji_reader = csv.DictReader(emoji_file)
        return {normalize_emoji_name(row["name"]): row["emoji"] for row in emoji_reader}


def normalize_emoji_name(name: str):
    if "face" in name:
        return name.split()[0]


def main():
    print("Reloading...")
    token_file = SECRETS_DIR / "token.txt"
    id_file = SECRETS_DIR / "client_id.txt"
    Bot(id_file.read_text()).run(token_file.read_text())


class Bot(discord.Client):
    def __init__(self, client_id: str, **kwargs):
        self.client_id = client_id
        super().__init__(**kwargs)

    def avalible_emoji(self) -> typing.Dict[str, typing.List[Emoji]]:
        return global_emoji()

    async def on_message(self, message: discord.Message):
        print(self.user.display_name)
        if message.author == self.user:
            return
        words = set(message.content.split())
        for emoji in (
            emoji for name, emoji in self.avalible_emoji().items() if name in words
        ):
            await message.add_reaction(emoji)

    async def on_ready(self):
        client_id = SECRETS_DIR / "client_id.txt"
        permissions = 2048
        invite_link = f"https://discordapp.com/oauth2/authorize?&client_id={client_id.read_text()}&scope=bot&permissions={permissions}"
        print(f"Bot running! Invite me at {invite_link}")


if __name__ == "__main__":
    main()
