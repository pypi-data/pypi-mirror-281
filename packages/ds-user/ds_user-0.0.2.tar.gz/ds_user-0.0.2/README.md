This library will make it easier to manage Discord accounts with an account token!

# Examples:

### Send Message

```python
from pydsacc.main import Account

client = Account(token="Your_ds_account_token")

client.send_message(channel_id=Channel_id, text="Hi")
```

### Delete Message

```python
from pydsacc.main import Account

client = Account(token="Your_ds_account_token")

client.delete_message(channel_id=Channel_id, message_id=Message_id)
```

### List Guilds

```python
from pydsacc.main import Account

client = Account(token="Your_ds_account_token")

guilds = client.list_guilds()

print(guilds)
```

### Get Channel Messages

```python
from pydsacc.main import Account

client = Account(token="Your_ds_account_token")

messages = client.get_channel_messages(channel_id=Channel_id)

print(messages)
```

### Delete Guild

```python
from pydsacc.main import Account

client = Account(token="Your_ds_account_token")

client.delete_guild(guild_id=Guild_id)
```
