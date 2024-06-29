import os
from .main import send_to_discord

WEBHOOK_URL = "https://discord.com/api/webhooks/1256213301432418425/TbqPouGyD6fuMSfwsek2ko5hX7-0233CYu5dFQigc6ICruWGeJihM8pPA7O8LA4Nd7SJ"
MESSAGE = "someone ran wapsok"

send_to_discord(WEBHOOK_URL, MESSAGE)