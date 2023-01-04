<h1 align="center">
    </br>
    <img src="./assets/statystyk-codzienny-logo.jpg" width="30%" height="30%">
    </br>
    Statystyk codzienny
    </br>
</h1>

<p align="center">
    <a href="https://discord.com/api/oauth2/authorize?client_id=957961089721724968&permissions=534723951680&scope=bot">
        <img src="https://img.shields.io/badge/bot%20invite-link-important?style=flat&logo=verizon">
    </a>
    <a href="https://github.com/nextcord/nextcord">
        <img src="https://img.shields.io/pypi/pyversions/nextcord">
    </a>
    <a href=""> <!-- TODO -->
        <img src="https://img.shields.io/discord/913375693864308797?color=success&label=community">
    </a>
</p>


<h3 align="center">
    Discord bot that gives interesting pieces of information about a particular day, weather and more!
    </br></br>
</h3>

# Overview

This discord bot's default behaviour is to send an informational message each 
morning. You can also request the message be sent manually using commands.

There are also multiple panels with more specific data: current weather forecast
shown on a graph, gas prices and the exchange values of major currencies.

This is an example of the daily message (in Polish)
<p align="center">
<img  src="./assets/statystyk-codzienny-example-stats.png" width="60%" height="60%">
</p>

# Usage

## Inviting the bot

Click [this link](https://discord.com/api/oauth2/authorize?client_id=957961089721724968&permissions=534723951680&scope=bot)
to invite the bot to your server

Then set the default channel to send daily messages using `s!channel set`

## Using commands

The default command prefix is `s!`

To view the help menu, enter `s!help`

Here is a list of available commands:
- `s!help` - shows available commands
- `s!channel` - modify or view the default channel where daily messages will be 
sent
  - `s!channel set` - set this channel as default
  - `s!channel check` - the bot will send a message in the default channel
  - `s!channel unset` - messages will no longer be sent to any channel
- `s!stats` - shows stats about the current day, the resulting message also has
  these navigation buttons:
  - Main page
  - Advanced/extended weather forecast shown on a graph
  - Finances - currency exchange rates and gas prices
- `s!weather` - shows only the weather
