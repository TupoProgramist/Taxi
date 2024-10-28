import json
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetChannelRecommendationsRequest
from telethon.tl.types import InputPeerChannel

# Function to load credentials from config.json
def load_credentials():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
        return config['api_id'], config['api_hash'], config['phone_number']

# Load credentials
api_id, api_hash, phone_number = load_credentials()

# Start the client
client = TelegramClient('17 September', api_id, api_hash)

async def get_channel_recommendations(channel_username):
    # Connect to the client
    await client.start(phone_number)

    try:
        # Fetch the channel entity using the username
        channel = await client.get_entity(channel_username)
        if isinstance(channel, InputPeerChannel):
            result = await client(GetChannelRecommendationsRequest(channel=channel, hash=0))
            print("Recommended Channels:")
            for rec_channel in result.chats:
                print(f"- {rec_channel.title} (@{rec_channel.username})")
        else:
            print(f"{channel_username} is not a valid channel.")
    except Exception as e:
        print(f"Error fetching recommendations: {str(e)}")
    finally:
        await client.disconnect()

# Replace with the username of the channel for which you want recommendations
channel_username = '@telegram'

# Run the async function
with client:
    client.loop.run_until_complete(get_channel_recommendations(channel_username))
