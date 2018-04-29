from microsoftbotframework import MsBot
from tasks import *

bot = MsBot()
bot.add_process(echo_response)

if __name__ == '__main__':
    bot.run()
