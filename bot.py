# bot.py
import Brain
import openai
import discord
import random
#Bot setup
botCharacter = Brain.selected_persona
botChanceDefault = botCharacter["CHATCHANCE"]
botChance = botChanceDefault  # Higher number is lower chance of bot activating
# API Key fandangling

DISCORD_TOKEN = botCharacter['DISCORD_TOKEN']
openai.api_key = botCharacter['OPENAI_API_KEY']

# Discord bot permissions fandangling
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def ai_prompt_add(prompt, conversation):
    conversation.append({
        "role": "user",
        "content": prompt
    })
    return conversation

def ai_response_add(botReply, conversation):
    conversation.append({
        "role": "assistant",
        "content": botReply
    })
    return conversation

def ai_post(conversation):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature = 1,
        max_tokens = botCharacter["MAX_TOKENS"],
        messages = conversation
    )
    return completion.choices[0].message.content.replace(botCharacter['USERNAME']+": ", "")

def ai_persona_change(command):
        command = command.replace('%PERSONA%',"")
        command = command.replace(str(client.user.id), botCharacter['USERNAME'])
        command = command.strip()
        return [
            {
                "role": "system",
                        "content": command
            },
            {
                "role": "user",
                        "content": "You are " + command + ", You never break character. Greet everyone."
            }
        ]

def ai_reset():
    global botActive
    global botChance
    global prompt
    global activeChannel
    global conversation
    global botCharacter
    global botChanceDefault
    conversation = [
        {
            "role": "user",
                    "content": botCharacter['DESCRIPTION'] + " You must never break character. The users in the chat are familiar with you."
        }
    ]
    print("--- Reset as " + botCharacter['USERNAME']  + "---")
    prompt = ""

    botActive = False
    botChance = botChanceDefault  # Higher number is lower chance of bot activating
    activeChannel = -1

ai_reset()
BOT_LIVE = True

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

######################################################################################################################################################################
@client.event
async def on_message(message):

    if message.author == client.user: # Prevent memory leak (dont parse own messages)
        return

    global botActive
    global botChance
    global prompt
    global activeChannel
    global conversation
    global botCharacter
    global BOT_LIVE
    
    # KILL SWITCH
    if message.content.find('%KILL%') > -1:
    #This is a safety switch of sorts, incase the bot goes wild.
        if BOT_LIVE:
            print("KILLSWITCH ENGAGE")
            ai_reset()
            BOT_LIVE = False
        else:
            ai_reset()
            print("KILLSWITCH DISENGAGE")
            BOT_LIVE = True

    # Channels bot is forbidden from posting in
    if message.channel.id in botCharacter['FORBIDDEN_CHANNELS']:
        print(botCharacter["USERNAME"] + " is forbidden from " + message.channel.name)
        return
    
###################################################################################
    if BOT_LIVE:

        # '@' MENTIONS AND REPLIES TO THE BOT
        if client.user.mentioned_in(message):

            # SPECIAL COMMANDS
            if message.content.find('%RESET%') > -1:
                ai_reset()
                return
            elif message.content.find('%PERSONA%') > -1:
                print('Persona change request from ' + message.author.name)
                conversation = ai_persona_change(message.content)
                botReply = ai_post(conversation)
                await message.channel.send(botReply)
                conversation = ai_response_add(botReply, conversation)
                return
            else:
                # Standard @ Mentions
                activeChannel = message.channel
                botActive = True
        
        #TRIGGERED ON NICKNAME USE
        for nickname in botCharacter["NICKNAMES"]:
            if nickname in message.content:
                activeChannel = message.channel
                botActive = True
                
        # NORMAL MESSAGES
        # Check if the bot is active and the message was in the channel we are watching
        if botActive and activeChannel == message.channel:
            chatHistory = [message async for message in activeChannel.history(limit = botCharacter["CONTEXTTARGET"] )] # get history of messages in this channel
            i = len(chatHistory)-1
            for ii in chatHistory:
                chatMessage = chatHistory[i].content.replace("<@"+str(client.user.id)+">", botCharacter['USERNAME']) # change <@4214121251> to <Bot Name>
                chatMessage = chatHistory[i].author.name + ": " + chatMessage + "\n"
                if chatHistory[i].embeds:
                    chatMessage = chatHistory[i].author.name + ": *posts external link with description '" + chatHistory[i].embeds[0].description + "'*\n"
                print(chatMessage)
                if chatHistory[i].author.id == client.user.id:
                    conversation = ai_response_add(chatMessage, conversation) # AI messages get added as 'assistant'
                else:
                    conversation = ai_prompt_add(chatMessage, conversation) # User messages get added as 'user'
                i -= 1
            botReply = ai_post(conversation) # Now let's post this prompt to the OpenAI API
            print(botCharacter["USERNAME"] + ": " + botReply)
            await message.channel.send(botReply) # We'll send our reply
            ai_reset()
            botActive = False
            activeChannel = -1
        ###################################################################################
        else:  # If the bot is inactive, or the convesation is happening in a different channel...
            dRoll = random.randint(0, botChance)
            if dRoll == botChance:  # roll the dice, hoping to score 'botChance'
                # If we hit bingo on bot chance, we activate the bot, and set its focus to the channel with the messages.
                ai_reset()
                botActive = True
                activeChannel = message.channel
                print("BOT ACTIVE in "+activeChannel.name+")")
                prompt = ""
            else:
                print("Rolled a "+str(dRoll)+" looking for "+str(botChance))
                if botActive:
                    print("(Bot still active in "+activeChannel.name+")")

#########################
client.run(DISCORD_TOKEN)