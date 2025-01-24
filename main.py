from bot.bot_handler import setup_bot
from utils.logger import setup_silent_logging
from dotenv import load_dotenv

load_dotenv()
setup_silent_logging()

if __name__ == "__main__":
    bot = setup_bot()
    print("🤖 Bot en ejecución (silencioso)")
    bot.run_polling()