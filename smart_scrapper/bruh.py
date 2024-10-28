from telethon.sync import TelegramClient
from telethon import functions, types

with TelegramClient("bruh", 26787318, "fed8f0bf35c374a0ebc0106618739e6a") as client:
    result = client(functions.channels.GetChannelRecommendationsRequest(
        channel='@pragmatikamedia'
    ))

    # Accessing the chats attribute of the result
    for channel in result.chats:
        print(channel.title)
