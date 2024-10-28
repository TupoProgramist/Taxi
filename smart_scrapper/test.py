import json
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import InputPeerChannel

# Function to load credentials from config.json
def load_credentials():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
        return config['api_id'], config['api_hash'], config['phone_number']

# Load credentials
api_id, api_hash, phone_number = load_credentials()

# Start the client
client = TelegramClient('session_name', api_id, api_hash)

async def get_channel_info(channel_username):
    # Connect to the client
    await client.start(phone_number)

    try:
        # Fetch the channel entity using the username
        channel = await client.get_entity(channel_username)

        # Use GetFullChannelRequest to get channel details including channel_id and access_hash
        full_channel = await client(GetFullChannelRequest(channel=channel))

        # Extract channel_id and access_hash
        channel_id = full_channel.chats[0].id
        channel_hash = full_channel.chats[0].access_hash

        return channel_id, channel_hash

    except Exception as e:
        print(f"Error fetching channel info: {str(e)}")
    finally:
        await client.disconnect()

# Replace with the username of the channel for which you want to get ID and hash
channel_username = InputPeerChannel(get_channel_info("IN OMNIA PARATUS"))


print("Recommended Channels:")
for rec_channel in result.chats:
    print(f"- {rec_channel.title} (@{rec_channel.username})")