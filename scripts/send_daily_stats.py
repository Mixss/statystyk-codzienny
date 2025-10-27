#!/usr/bin/env python3
"""
Standalone script to send daily statistics to Discord channels.
This script is designed to be run by GitHub Actions on a schedule.
"""

import asyncio
import os
import sys
import json
from pathlib import Path

# Add the parent directory to Python path to import project modules
sys.path.append(str(Path(__file__).parent.parent))

import nextcord
from logic.advanced_forecast import generate_graphs_image
from logic.forecast_image import generate_forecast_image
from ui import message_templates


async def get_channels_from_env():
    """
    Get Discord channels from environment variables.
    Expected format: DISCORD_CHANNELS='[{"ServerId": 123, "ChannelId": 456}, {"ServerId": 789, "ChannelId": 101112}]'
    """
    channels_env = os.getenv('DISCORD_CHANNELS')
    if not channels_env:
        # Fallback to config.json if env var not set
        config_path = Path(__file__).parent.parent / "data" / "config.json"
        if config_path.exists():
            with open(config_path) as file:
                data = json.load(file)
                return data.get("BroadcastChannels", [])
        return []
    
    try:
        return json.loads(channels_env)
    except json.JSONDecodeError as e:
        print(f"Error parsing DISCORD_CHANNELS environment variable: {e}")
        return []


async def send_daily_stats():
    """
    Send daily statistics to configured Discord channels.
    """
    # Get Discord bot token
    token = os.getenv('CLIENT_TOKEN')
    if not token:
        print("Error: CLIENT_TOKEN environment variable not found")
        return False

    # Get channels configuration
    channels = await get_channels_from_env()
    if not channels:
        print("Warning: No channels configured for broadcasting")
        return True

    # Generate forecast images
    print("Generating forecast images...")
    image_generated = False
    try:
        generate_forecast_image()
        generate_graphs_image()
        print("Images generated successfully")
        image_generated = True
    except Exception as e:
        print(f"Warning: Could not generate images: {e}")
        print("Continuing without images...")
        # Create a dummy image file so the script doesn't fail
        os.makedirs('./assets/generated_images', exist_ok=True)
        with open('./assets/generated_images/image.png', 'w') as f:
            f.write("dummy")  # Will be replaced with actual logic later

    # Initialize Discord client
    intents = nextcord.Intents.default()
    intents.message_content = True
    client = nextcord.Client(intents=intents)

    # Flag to track if we've sent messages
    sent_successfully = False

    @client.event
    async def on_ready():
        nonlocal sent_successfully
        print(f'Logged in as {client.user}')
        
        try:
            for channel_config in channels:
                channel_id = channel_config["ChannelId"]
                server_id = channel_config["ServerId"]
                
                channel = client.get_channel(channel_id)
                if not channel:
                    print(f"Warning: Could not find channel with ID {channel_id}")
                    continue

                print(f'Sending stats to #{channel.name} (ID: {channel_id}) in server {server_id}')

                # Create embed
                embed = await message_templates.daily_stats_embed(
                    'image.png',  # filename for embed
                    our_server=(server_id == 913375693864308797)  # OUR_SERVER_ID constant
                )

                # Only send image if it was generated successfully
                if image_generated and os.path.exists('./assets/generated_images/image.png'):
                    forecast_image = nextcord.File('./assets/generated_images/image.png')
                    await channel.send(embed=embed, files=[forecast_image])
                else:
                    await channel.send(embed=embed)
                    
                print(f'Successfully sent daily stats to #{channel.name}')

            sent_successfully = True
            print("All messages sent successfully")
            
        except Exception as e:
            print(f"Error sending messages: {e}")
        
        finally:
            await client.close()

    # Start the client
    try:
        await client.start(token)
    except Exception as e:
        print(f"Error starting Discord client: {e}")
        return False

    return sent_successfully


async def main():
    """Main entry point for the script."""
    # Check for test mode
    test_mode = len(sys.argv) > 1 and sys.argv[1] == '--test'
    
    if test_mode:
        print("Running in test mode...")
        # Test channel configuration
        channels = await get_channels_from_env()
        print(f"Found {len(channels)} channels configured:")
        for channel in channels:
            print(f"  - Server ID: {channel['ServerId']}, Channel ID: {channel['ChannelId']}")
        
        # Test token
        token = os.getenv('CLIENT_TOKEN')
        if token:
            print("✓ CLIENT_TOKEN found")
        else:
            print("✗ CLIENT_TOKEN not found")
        
        print("Test completed successfully!")
        return
    
    print("Starting daily stats broadcast...")
    success = await send_daily_stats()
    
    if success:
        print("Daily stats sent successfully!")
        sys.exit(0)
    else:
        print("Failed to send daily stats")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())