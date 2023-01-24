import nextcord
from nextcord import InteractionMessage
from nextcord.ext.commands import Bot


class MessageEditHandler:
    last_message: InteractionMessage | None = None

    @staticmethod
    async def edit_message(client: Bot, channel_id: int, message_id: int, content: str, embed=None, view=None,
                           files=None):
        channel = client.get_channel(channel_id)
        message = await channel.fetch_message(message_id)

        # includes files
        if files:
            await message.edit(content=content, embed=embed, view=view, files=[nextcord.File(f) for f in files])
        else:
            await message.edit(content=content, embed=embed, view=view)
