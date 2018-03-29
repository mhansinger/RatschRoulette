# main file to run the messageing bot

from MessageBot import MessageBot
from telepot.loop import MessageLoop

if __name__ == '__main__':
    myBot = MessageBot()
    MessageLoop(myBot.bot, myBot.handle).run_as_thread()
    print('Listening ...')
