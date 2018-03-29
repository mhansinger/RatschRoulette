# main file to run the messageing bot

from MessageBot import MessageBot
from telepot.loop import MessageLoop

myBot = MessageBot()

if __name__ == '__main__':

    MessageLoop(myBot.bot, myBot.handle).run_as_thread()
    print('Listening ...')
