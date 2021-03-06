import secrets
import sys
from multiprocessing import Process

import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import game_tracker
import message_handler
import settings
from bot_events import *  # pylint: disable=unused-wildcard-import
from bot_events.base_event import BaseEvent

# Set to remember if the bot is already running, since on_ready may be called
# more than once on reconnects
this = sys.modules[__name__]
this.running = False

# Scheduler that will be used to manage events
sched = AsyncIOScheduler()


###############################################################################

def main():
    # Initialize the client
    print("Starting up...")
    client = discord.Client()

    # Define event handlers for the client
    # on_ready may be called multiple times in the event of a reconnect,
    # hence the running flag
    @client.event
    async def on_ready():  # pylint: disable=unused-variable
        if this.running:
            return

        this.running = True

        # Set the playing status
        if settings.NOW_PLAYING:
            print("Setting NP game", flush=True)
            await client.change_presence(
                activity=discord.Game(name=settings.NOW_PLAYING))
        print("Logged in!", flush=True)

        # Load all events
        print("Loading events...", flush=True)
        n_ev = 0
        for ev in BaseEvent.__subclasses__():
            event = ev()
            sched.add_job(event.run, 'interval', (client,),
                          minutes=event.interval_minutes)
            n_ev += 1
        sched.start()
        print(f"{n_ev} events loaded", flush=True)

        if game_tracker.global_tracker != None:
            print(f'{len(game_tracker.global_tracker.supported_games)} game(s) loaded: \n{game_tracker.global_tracker.supported_games}')

    # The message handler for both new message and edits
    async def common_handle_message(message):
        text = message.content
        if text.startswith(settings.COMMAND_PREFIX) and text != settings.COMMAND_PREFIX:
            cmd_split = text[len(settings.COMMAND_PREFIX):].split()
            try:
                await message_handler.handle_command(cmd_split[0].lower(),
                                                     cmd_split[1:], message, client)
            except:
                print("Error while handling message", flush=True)
                raise

    @client.event
    async def on_message(message):  # pylint: disable=unused-variable
        await common_handle_message(message)

    @client.event
    async def on_message_edit(before, after):  # pylint: disable=unused-variable
        await common_handle_message(after)

    # Finally, set the bot running
    client.run(secrets.BOT_TOKEN)

###############################################################################


if __name__ == "__main__":
    main()
