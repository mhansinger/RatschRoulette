# main file to run the messageing bot

from RouletteBot import RouletteBot
from telepot.loop import MessageLoop

myBot = RouletteBot()

if __name__ == '__main__':

    MessageLoop(myBot.bot, myBot.handle).run_as_thread()
    print('Listening ...')
