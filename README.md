# Rolebot
Purpose is to link games and roles on Discord. You no longer need to ping each friend individually; by using, for example, `@game_deadlock` ping everyone with that role will be notified. On the server, there is a message where reacting with an emoji allows the bot to assign a role. Admins can add emoji-role pairs using a command like `!add_gamerole 🧙‍♂️ dota2`, so that everyone who reacts to the message with the 🧙‍♂️ emoji will also receive the dota2 role.


## Installation and running:
```
pip3 install -r requirements.txt 
python3 rolebot.py
```
   
Note: The bot requires permissions to manage roles and send messages.

## Usage:
Create a new game role
* Requires an Admin role
* Type in the channel (or to the bot): `!add_gamerole 🧙‍♂️ overwatch`, for example. That is, a command followed by an emoji and the game's name. Now, when this emoji is used on the specified message, the bot will assign the role associated with the emoji to the user.

Role mappings are saved (and loaded) from the `role_mapping.json` file.

## Configuration:
Open `.env.example` and fill in the following: 

`DISCORD_TOKEN = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` Your Discord bot token. 

`MESSAGE_ID = 12345678901234567890` The ID of the message whose reactions the bot will monitor.

`CHANNEL_ID = 133713371337` The channel where the bot will notify if someone has added a specific game role to themselves. Setting this to, e.g., 0 will disable notifications.

`ADMIN_ROLE = xxxxx` The name of the role that acts as admin (allows creating new emoji-game role combinations).

`ROLE_PREFIX = game_` The prefix used to distinguish game roles from other server roles.

And then save the file as  `.env`
