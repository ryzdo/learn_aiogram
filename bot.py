
from config_data.config import load_config


config = load_config(None)

bot_token = config.tg_bot.token
superadmin = config.tg_bot.admin_id[0]
print(bot_token)
