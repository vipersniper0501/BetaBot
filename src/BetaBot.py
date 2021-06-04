import asyncio
import datetime
import pprint
import discord
import pathlib
import json
import random

client = discord.Client()

    
@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    # CyberGuild = ''
    # for guild in client.guilds:
    #     print(guild)
    #     print(guild.id)
    #     if guild.id == 638764512966606864:
    #         CyberGuild = guild
    #         print(f'CyberGuild ID: {CyberGuild.id}')
    #         break
    loop = asyncio.get_event_loop()
    bg_task = loop.create_task(background_tasks())


async def background_tasks():
    with open("reminders.json") as f:
            reminders = json.load(f)    # List of dates and times for meetings
    channel = client.get_channel(751738418253529098)  # CyberPatriots Announcements Channel
    while True:
        x = datetime.datetime.now()
        print(x.strftime("%X"))
        guild = client.guilds[0]
        print(guild)
        for key, value in reminders["Competition Rounds"].items():
            if "Not Started" in value["Status"]:
                # print(f'key = {key}, value = {value}')
                print('Next Competition Not Started')
                last_meeting = value["Last Meeting"].split(", ")[1] # Date of last meeting before next competition day
                current_date = f'{x.strftime("%B")} {x.strftime("%-d")}' # current date to compare with
                if current_date == last_meeting:
                    await channel.send(f'This is the last Tuesday CyberPatriot meeting before {key}! Make sure you are prepared and good luck!')
                    value["Status"] = "Starting Soon"
                    break
            elif "Starting Soon" in value["Status"]:
                print('Next Competition Starting Soon')
                start_date = value["Competition Round"]["Start"].split(", ")[1]
                current_date = f'{x.strftime("%B")} {x.strftime("%-d")}'
                if current_date == start_date:
                    await channel.send(f'{key} is starting around the world! Are you ready?')
                    value["Status"] = "Running"
                    break
            elif "Running" in value["Status"]:
                print('Competition is currently running')
                start_date = value["Competition Round"]["End"].split(", ")[1]
                current_date = f'{x.strftime("%B")} {x.strftime("%-d")}'
                if current_date == start_date:
                    await channel.send(f'{key} has been completed!')
                    value["Status"] = "Completed"
                    break
        if x.strftime("%A") in reminders:    # Checks if current day of the week is in list
            print(x.strftime("%A"))
            print(reminders[x.strftime("%A")]["Role"])
            role = guild.get_role(int(reminders[x.strftime("%A")]["Role"]["id"]))    # Role that will be mentioned
            print(role)
            current_time_buffer = x.strftime("%X").split(':')
            current_time = f"{current_time_buffer[0]}:{current_time_buffer[1]}:00"   # Rounds down current time to the minute.
            print(current_time)
            if current_time in reminders[x.strftime("%A")]["Time"]:
                try:
                    print('Sending Notification to Cyberpatriots notification channel...')
                    await channel.send(
                        f'The time is currently {x.strftime("%X")}, and the {role.mention} meeting starts in **5 minutes!** Meeting link is: {reminders[x.strftime("%A")]["Meeting"]}')
                except Exception as e:
                    print(e)
        await asyncio.sleep(60)  # runs every 60 seconds
  
@client.event
async def on_message(message):
    storage_file = pathlib.Path("list_store.json")
    if storage_file.is_file():
        with open(storage_file) as f:
            BETA_Taskmaster = json.load(f)
       
    if message.author == client.user:
        return
        
    if message.content == '--BETA':
        phrases = ['I am BETA', 'BETA > Alpha', 'You dare challenge the authority of BETA?!',
                       'I am clearly not in beta testing.', 'Why are you calling my name?']
        await message.channel.send(random.choice(phrases))
        
    add_prefix = '--BETA-add-t'
    if message.content.startswith(add_prefix):
        if str(message.author.id) not in BETA_Taskmaster:
            print('New User...')
            BETA_Taskmaster[str(message.author.id)] = {"Username": message.author, "Tasks": []}
            content = BETA_Taskmaster[str(message.author.id)]['Tasks']
            taskID = str(len(content))
            content[f"{taskID}"] = message.content[len(add_prefix) + 1:].strip()
            with open("list_store.json", mode = 'w') as f:
                json.dump(BETA_Taskmaster, f, indent = 4)
            await message.channel.send('Stored Item')
            print('Item Successfully Stored')
        else:
            print('Returning User...')
            content = BETA_Taskmaster[str(message.author.id)]['Tasks']
            taskID = str(len(content))
            content[f"{taskID}"] = message.content[len(add_prefix) + 1:].strip()
            with open("list_store.json", mode = 'w') as f:
                json.dump(BETA_Taskmaster, f, indent = 4)
            await message.channel.send('Item Successfully Stored')
            print('Item Successfully Stored')
      
    rm_prefix = "--BETA-rm-t"
    if message.content.startswith(rm_prefix):
        content = BETA_Taskmaster[str(message.author.id)]['Tasks']
        taskID = message.content[len(rm_prefix) + 1:].strip()
        try:
            content.pop(str(taskID))
        except Exception:
            await message.channel.send('Uh Oh! Item not found!')
            return
        for i in range(0, len(content)):
            buffer = list(content.values())[0]  # Stores current value of current index's key.
            print(f'Buffer : {buffer}')
            content.pop(str(list(content)[0]))  # Pops current key and value
            print(content)
            content[
                f"{i}"] = buffer  # Rebuilds key with value stored in buffer, and adds the value to the end of the dictionary.
            print(content)
            # After loop completes, dictionary stored in JSON file should now be ordered correctly.
        with open("list_store.json", mode = 'w') as f:
            json.dump(BETA_Taskmaster, f, indent = 4)
        await message.channel.send('Item Successfully Removed!')
       
    if message.content == '--BETA-l-t':
        content = BETA_Taskmaster[str(message.author.id)]['Tasks']
        send = "Key  :  Task \n"
        for i in range(0, len(content)):
            send = send + f"{i} : " + content[str(i)] + '\n'
        embed = discord.Embed(
            title = message.author.display_name + ' Tasks: ',
            description = send
        )
        # Bot fails to print logged tasks that are in list_json file
        await message.channel.send(embed = embed)
        
    eightball_prefix = '--BETA-8Ball '
    if message.content.startswith(eightball_prefix):
        message_output = ["As I see it, yes.", "Ask again later.", "Better not tell you now.",
                          "Cannot predict now.",
                          "Concentrate and ask again.", "Don't count on it.", "It is certain.",
                          "It is decidedly so.",
                          "Most likely.", "My reply is no.", "My sources say no.",
                          "Outlook not so good.",
                          "Outlook good.",
                          "Reply hazy, try again.", "Signs point to yes.", "Very doubtful.",
                          "Without a doubt.", "Yes.",
                          "Yes - definitely.", "You may rely on it.", "No, definitely not."]
        await message.channel.send(random.choice(message_output))
        
    if message.content == '--BETA-Help':
        embed = discord.Embed(
            title = "BetaBot Help:",
            description = """
            This is a list of commands that I.... BETA... support:
            1.) --BETA-Help : List of helpful commands
            2.) --BETA : Says 'I am BETA'
            3.) --BETA-add-t : adds task to your personal list of items
            4.) --BETA-rm-t <key> : Removes task from your personal list of items
            4.) --BETA-l-t: Lists your personal tasks
            5.) --BETA-8Ball : Eight ball. Ask me a question.
            6.) --BETA-Reminder : Times for after school CyberPatriots meetings
            """
        )
        await message.channel.send(embed = embed)
      
    if message.content == '--BETA-Reminder' or message.content == '--BETA-Reminders':
        with open("reminders.json") as f:
            reminders = json.load(f)
        print(reminders)
        pp = pprint.PrettyPrinter(indent=4, sort_dicts=False)
        printer = pp.pformat(reminders)
        test = json.dumps(reminders, 
                indent = 2,
                sort_keys = False)
        print(test)
        descriptions = "Day of the week : Time, Class, Meeting link \n"
        for key, value in reminders.items():
            descriptions = descriptions + f"{key} : {value}\n"
        embed = discord.Embed(
            title = "After School Meeting Reminders:",
            description = test
        )
        await message.channel.send(embed=embed)


def main():
    with open('./token.txt') as f:
        token = f.read().strip()
#    client = BetaBot()
    client.run(token)

if __name__ == '__main__':
    main()
