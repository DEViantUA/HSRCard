# Import necessary modules
from hsrcard import hsr
import asyncio

# Define the main function that fetches information about a player using a specified UID
async def main(uid):
  async with hsr.HonkaiCard() as hmhm:
    result = await hmhm.creat(uid)
  print(result)

  # Output explanation:
  # settings:
  # uid=800293940 - UID (unique identifier) of the player is 800293940.
  # lang='en' - the game language is set to English.
  # hide=False - player profile information is not hidden.
  # save=True - information saving setting is enabled.
  # background=None - no background image.
  #
  # player:
  # uid='700649319' - player's UID is 700649319.
  # nickname='Korzzex' - player's nickname is "Korzzex".
  # level=69 - player's level is 69.
  # avatar - information about the player's avatar:
  # id='201212' - avatar identifier.
  # name='Jingliu' - avatar name is "Jingliu".
  # icon - URL of the avatar image.
  # signature="----".
  # friend_count=39 - the player has 39 friends.
  # world_level=6 - player's world level is 6.
  #
  # card (list of player's character cards):
  # Card(id='1212', name='Jingliu', rarity=5, card=<PIL.Image.Image ...): Information about the "Jingliu" character card:
  # id='1212' - card identifier.
  # name='Jingliu' - character name.
  # rarity=5 - card rarity is 5.
  # card - card image.
  # (similar entries for other character cards).
  #
  # name - list of character names separated by commas: "Jingliu, Silver Wolf, Seele, Luocha".
  #
  # id - list of character card identifiers separated by commas: "1212, 1006, 1102, 1203".

# Call the main function with UID 700649319
asyncio.run(main(700649319))
