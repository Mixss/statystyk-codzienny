#!/usr/bin/env python3
"""
Simple verification script to test environment variable parsing and basic logic
without requiring nextcord dependencies.
"""

import os
import sys
import json
from pathlib import Path

# Add the parent directory to Python path to import project modules
sys.path.append(str(Path(__file__).parent.parent))


def test_env_channels():
    """Test environment variable channel parsing."""
    print("Testing environment variable channel parsing...")
    
    # Test with no environment variable
    channels_env = os.getenv('DISCORD_CHANNELS')
    if not channels_env:
        print("✓ No DISCORD_CHANNELS environment variable set (expected)")
        
        # Test fallback to config.json
        config_path = Path(__file__).parent.parent / "data" / "config.json"
        if config_path.exists():
            with open(config_path) as file:
                data = json.load(file)
                channels = data.get("BroadcastChannels", [])
                print(f"✓ Fallback to config.json: found {len(channels)} channels")
                for channel in channels:
                    print(f"  - Server ID: {channel['ServerId']}, Channel ID: {channel['ChannelId']}")
        else:
            print("✗ config.json not found")
    else:
        try:
            channels = json.loads(channels_env)
            print(f"✓ Environment variable parsed: found {len(channels)} channels")
            for channel in channels:
                print(f"  - Server ID: {channel['ServerId']}, Channel ID: {channel['ChannelId']}")
        except json.JSONDecodeError as e:
            print(f"✗ Error parsing DISCORD_CHANNELS: {e}")


def test_client_token():
    """Test CLIENT_TOKEN environment variable."""
    print("\nTesting CLIENT_TOKEN environment variable...")
    
    token = os.getenv('CLIENT_TOKEN')
    if token:
        print("✓ CLIENT_TOKEN found")
        print(f"  Token length: {len(token)} characters")
        print(f"  Token preview: {token[:20]}..." if len(token) > 20 else f"  Token: {token}")
    else:
        print("✗ CLIENT_TOKEN not found")


def test_file_structure():
    """Test required file and directory structure."""
    print("\nTesting file structure...")
    
    base_path = Path(__file__).parent.parent
    
    required_paths = [
        "data/config.json",
        "data/deadlines",
        "assets/generated_images",
        "ui/message_templates.py",
        "logic/logic.py",
        "logic/forecast_image.py",
        "logic/advanced_forecast.py"
    ]
    
    for path_str in required_paths:
        path = base_path / path_str
        if path.exists():
            print(f"✓ {path_str} exists")
        else:
            print(f"✗ {path_str} missing")


def main():
    """Run all verification tests."""
    print("=== Statystyk Daily Bot Verification ===\n")
    
    test_env_channels()
    test_client_token()
    test_file_structure()
    
    print("\n=== Verification Complete ===")


if __name__ == "__main__":
    main()