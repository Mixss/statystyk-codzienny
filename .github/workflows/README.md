# GitHub Actions Setup for Daily Stats Bot

This directory contains the GitHub Actions workflow for automated daily statistics broadcasting.

## Workflow: Daily Stats Broadcast

The workflow (`daily-stats.yml`) is configured to:

- Run daily at 4:30 AM UTC (matching the original schedule)
- Send daily statistics to Discord channels specified in environment variables
- Can be triggered manually for testing purposes

## Required Secrets

Configure the following secrets in your GitHub repository settings:

### CLIENT_TOKEN
The Discord bot token for authentication.

### DISCORD_CHANNELS
JSON array containing channel configurations. Format:
```json
[
  {
    "ServerId": 913375693864308797,
    "ChannelId": 958119472793780304
  },
  {
    "ServerId": 465940323365814272,
    "ChannelId": 828951713074380840
  }
]
```

## Manual Triggering

You can manually trigger the workflow from the GitHub Actions tab in your repository by selecting "Daily Stats Broadcast" and clicking "Run workflow".

## Dependencies

The workflow automatically installs:
- System dependencies (libjpeg-dev, zlib1g-dev)
- Python dependencies from requirements.txt
- Creates necessary directories

## Migration from Persistent Bot

This replaces the previous setup where the bot ran continuously and used internal scheduling. The new approach:

1. Uses GitHub Actions cron scheduling instead of nextcord tasks
2. Gets channel configuration from environment variables instead of config.json
3. Runs as a stateless process rather than a persistent bot
4. Provides better reliability and easier management