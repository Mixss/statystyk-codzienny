# Migration Guide: From Persistent Bot to GitHub Actions

This guide helps you migrate from running the bot as a persistent service to using GitHub Actions for daily scheduling.

## Why Migrate?

The GitHub Actions approach offers several advantages:

- **Lower resource usage**: No need to keep a bot running 24/7
- **Better reliability**: GitHub's infrastructure handles scheduling
- **Easier maintenance**: No need to manage hosting infrastructure
- **Cost-effective**: Only runs when needed

## Migration Steps

### 1. Export Current Channel Configuration

If you're currently using the persistent bot with `/channel set` commands, your channels are stored in `data/config.json`. You need to convert this to the environment variable format.

#### Current format (config.json):
```json
{
  "BroadcastChannels": [
    {
      "ServerId": 913375693864308797,
      "ChannelId": 958119472793780304
    },
    {
      "ServerId": 465940323365814272,
      "ChannelId": 828951713074380840
    }
  ]
}
```

#### Convert to environment variable format:
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

Simply copy the array inside `BroadcastChannels` from your config.json.

### 2. Set Up Repository Secrets

In your GitHub repository:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Create these repository secrets:
   - `CLIENT_TOKEN`: Your Discord bot token (same as before)
   - `DISCORD_CHANNELS`: The JSON array from step 1

### 3. Stop the Persistent Bot

- If using Heroku: Scale down the worker dyno or delete the app
- If using Docker: Stop the container
- If using direct hosting: Stop the `python main.py` process

### 4. Test the GitHub Actions Workflow

1. Go to the **Actions** tab in your repository
2. Find "Daily Stats Broadcast" workflow
3. Click "Run workflow" to manually trigger it
4. Check the logs to ensure it runs successfully

### 5. Verify Daily Schedule

The workflow is configured to run daily at 4:30 AM UTC. If you need a different time:

1. Edit `.github/workflows/daily-stats.yml`
2. Modify the cron expression: `'30 4 * * *'`
3. Commit the changes

### Cron Schedule Examples

- `'30 4 * * *'` - 4:30 AM UTC daily
- `'0 6 * * *'` - 6:00 AM UTC daily  
- `'30 7 * * *'` - 7:30 AM UTC daily
- `'0 12 * * *'` - 12:00 PM UTC daily

## Troubleshooting

### "No channels configured" error
- Check that `DISCORD_CHANNELS` secret is properly formatted JSON
- Ensure channel IDs and server IDs are numbers, not strings

### "CLIENT_TOKEN not found" error
- Verify the `CLIENT_TOKEN` secret is set in repository settings
- Make sure the bot token is valid and has necessary permissions

### "Could not find channel" warnings
- Verify channel IDs are correct
- Ensure the bot has access to the channels
- Check that the bot is still in the Discord servers

### Permission errors
- Make sure the bot has "Send Messages" and "Embed Links" permissions
- Verify the bot can access the specified channels

## Reverting to Persistent Bot

If you need to revert to the persistent bot approach:

1. Disable the GitHub Actions workflow:
   - Edit `.github/workflows/daily-stats.yml`
   - Comment out or remove the `schedule` trigger

2. Update your `data/config.json` with current channels:
   ```json
   {
     "BroadcastChannels": [
       // Copy from DISCORD_CHANNELS environment variable
     ]
   }
   ```

3. Deploy the bot using your preferred hosting method:
   - Heroku: Push to the heroku remote
   - Docker: Build and run the container
   - Direct: Run `python main.py`

## Support

If you encounter issues during migration:

1. Check the GitHub Actions logs for detailed error messages
2. Use the verification script: `python scripts/verify_setup.py`
3. Test environment variables locally (without Discord token)
4. Open an issue in the repository with logs and configuration details