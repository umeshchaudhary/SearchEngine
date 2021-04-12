from typing import Union, Awaitable
import logging
from logging.handlers import RotatingFileHandler
# noinspection PyPackageRequirements
import discord
import constants
import config as env_variables
from database_manager import DBManager
from interactions import interactions


client = discord.Client()


# noinspection PyArgumentList
@client.event
async def on_ready():
  await DBManager.setup_db()
  logging.info('We have logged in as {0.user}'.format(client))


# noinspection PyArgumentList
@client.event
async def on_disconnect():
  await DBManager.close()


@client.event
async def on_message(message: discord.message.Message):
  if message.author == client.user:
    return

  # extract the interaction type and the related message from user input
  # for ex: !google search it
  # here `!google` is the interaction type and `search it` is the message
  input_message_parts: list = message.content.strip().split(' ', 1)

  interaction_type: str = input_message_parts[0]
  interaction_handler: Union[Awaitable, str, None] = interactions.get(interaction_type, None)

  if not interaction_handler:
    await message.channel.send(constants.INVALID_INPUT)
    await message.channel.send('\n'.join(interactions.keys()))
    return

  # the returned object is not callable function or method then it probably contains the response text for the input
  if not callable(interaction_handler):
    await message.channel.send(interaction_handler)
    return

  success: bool = await interaction_handler(input_message_parts[1].strip(), message.channel)

  if not success:
    await message.channel.send(constants.INTERNAL_SERVER_ERROR)


if __name__ == '__main__':
  logger = logging.getLogger('discord')
  handler = RotatingFileHandler('discord.log',
                                mode='a', maxBytes=5 * 1024 * 1024,
                                backupCount=2, encoding='utf-8')
  log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
  handler.setFormatter(log_formatter)
  handler.setLevel(env_variables.LOG_LEVEL)
  logger.setLevel(env_variables.LOG_LEVEL)
  logger.addHandler(handler)
  client.run(env_variables.BOT_SECRET)
