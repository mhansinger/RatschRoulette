# main file to run the messageing bot

from MessageBot import MessageBot
from telepot.loop import MessageLoop

myBot = MessageBot()

def run_bot():

    MessageLoop(myBot.bot, myBot.handle).run_as_thread()
    print('Listening ...')
