import aiohttp
import random

class Account:
   def __init__(self, token: str):
      self.api_url = "https://discord.com/api/v9/"
      self.token = token

      self.headers = {
         'Authorization': f'{self.token}',
         'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.309 Chrome/83.0.4103.122 Electron/9.3.5 Safari/537.36',
         'Content-Type': 'application/json'
      }

   async def send_message(self, channel_id: int, text: str):
      payload = {
         "content": text,
         "flags": 0,
         "mobile_network_type": "unknown",
         "nonce": random.randint(100000000000000000,900000000000000000),
         "tts": False
      }

      async with aiohttp.ClientSession() as session:
         async with session.post(f"{self.api_url}channels/{channel_id}/messages", headers=self.headers, json=payload) as response:

            return await response.text()

   async def delete_message(self, channel_id: int, message_id: int,):
      async with aiohttp.ClientSession() as session:
         async with session.delete(f"{self.api_url}channels/{channel_id}/messages/{message_id}", headers=self.headers) as response:
            return await response.text()

   async def list_guilds(self):
      async with aiohttp.ClientSession() as session:
         async with session.get(f"{self.api_url}users/@me/guilds", headers=self.headers) as response:
            return await response.text()

   async def get_channel_messages(self, channel_id: int):
      async with aiohttp.ClientSession() as session:
         async with session.get(f"{self.api_url}channels/{channel_id}/messages", headers=self.headers) as response:
            return await response.text()

   async def delete_guild(self, guild_id: int):
      async with aiohttp.ClientSession() as session:
         async with session.post(f"{self.api_url}guilds/{guild_id}/delete", headers=self.headers) as response:
            return await response.text()