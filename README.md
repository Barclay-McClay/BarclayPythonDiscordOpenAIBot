# Discord Bot

This is an easily customisable platform for building your own OpenAI chatGPT-based Discord bot.

## Install

### Requirements

You need [Python](https://www.python.org/downloads/), an [OpenAI API key](https://platform.openai.com/), a [Discord application](https://discord.com/developers/applications/), and the following packages via `pip` in your terminal:
```
pip install discord.py
pip install openai
```

Open up `Brain.py` and add your [Discord Bot's token](https://discord.com/developers/applications/) and your [OpenAI API Key](https://platform.openai.com/account/api-keys)

### Running the bot

1. Use Discord's [OAuth2 URL Generator](https://discord.com/developers/applications/) to add your bot to your server.
2. Open a Terminal/PowerShell window,
3. Navigate to the folder containing this repo on your computer.
4. `py bot.py`
5. The bot will try to login with the `DISCORD_TOKEN` provided in the `Brain.py` file.

## Usage

### Build your own bot

Get familiar with `Brain.py` - create your own Python dictionary by using `captain_trips` or `hana` as a template, then set it to the `selected_persona` variable at the bottom of the script.

### Talking to the bot

The bot can be 'triggered' a number of different ways:
- `@BotUsername` messages
- Any message containing the bot's name, or one of the bot's nicknames.
- Every time a user sends a message in a channel the bot is active in, the bot will 'roll a dice'. If the bot rolls the highest number on this dice (`CHATCHANCE` in `Brain.py`), then it will trigger a response spontaneously.

If you have a server with a-lot messages regularly flying about- it is better to set `CHATCHANCE` very high. I recommend setting it to a number you think is 'too high'. The spontaneous messages are part of what makes this bot special; but it is a double-edged sword, as the messages *are* disruptive. It is better if they are isolated to rare-occurances (keep them 'special'). An overly verbose and chatty bot *will* clear a room/kill conversation in a server. Moderation is key.

### Notes on API usage:

This app makes use of the `gpt-3.5-turbo` OpenAI model. It is currently the cheapest (and best suited) model available on the platform. At time of writing, it is priced at [$0.002 per 1K tokens](https://openai.com/pricing)

Anecdotally, while developing the bot, I made **a-lot** of API calls, and spent what *felt* like was **a-lot** of tokens doing so; but I never exceeded $1 in API credit. Messages are cheap- **but beware**- if two of these bots start talking to eachother, they will *never* tire. If left unsupervised in the same room, you could go to bed, and they will talk all night while you sleep. When you wake up- all of those API calls will have cost you money.

*This bot is easily exploitable and should not be deployed in servers where you do not have full control, and/or run the risk of exposing it to bad actors.*

## Feedback

I'd love to hear from you!
I developed this with the intention of it sitting it in a small (<20 people) server. But am interested in how it scales/what use-cases you have found for it.

I have built more complicated, 'bespoke' bots for different use-cases, by layering additional functionality on-top of this codebase.
If you have ideas/requests/criticisms, [I invite you to drop by the little development playground where I test/deploy my Discord apps and have a chat anytime.](https://discord.gg/JvWD5TdgkD)

Enjoy 🙌
