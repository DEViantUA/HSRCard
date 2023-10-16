# Copyright 2023 DEViantUa <t.me/deviant_ua>
# All rights reserved.

from PIL import Image,ImageDraw
from ..tools import pill
import asyncio

class Info:
    def __init__(self, character, cache, lang) -> None:
        """
        Initializes an Info object with character information, cache, and language settings.
        
        :param character: Information about the character.
        :param cache: A cache for storing data.
        :param lang: Language settings and translations.
        """
        self.character = character
        self.cache = cache
        self.lang = lang

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass
    
    async def get_max_lvl(self):
        """
        Determines the maximum character level based on the character's promotion.
        
        :return: The maximum character level (integer).
        """
        if self.character.promotion == 0:
            max = 20
        elif self.character.promotion == 1:
            max = 30
        elif self.character.promotion == 2:
            max = 40 
        elif self.character.promotion == 3:
            max = 50
        elif self.character.promotion == 4:
            max = 60
        elif self.character.promotion == 5:
            max = 70
        else:
            max = 80
        
        return max
 
    async def creat_holst(self, name_light_cone, icon_element, icon_path, max_level):
        """
        Creates a composite image with character information, icons, and background.
        
        :param name_light_cone: The background image for character information.
        :param icon_element: The element icon image.
        :param icon_path: The path icon image.
        :param max_level: The maximum character level.
        :return: A composite image with character information (PIL.Image.Image).
        """
        font = await pill.get_font(29)
        
        level = f"{self.lang.lvl}: {self.character.level}/{max_level}"
        x = int(font.getlength(level))
        
        holst = Image.new("RGBA", (437, name_light_cone.size[1] + 100), (0, 0, 0, 0))
        
        draw = ImageDraw.Draw(holst)
        draw.text((1, name_light_cone.size[1] - 20), level, font=font, fill=(255, 255, 255, 255))
        
        holst.alpha_composite(name_light_cone)
        
        holst.alpha_composite(icon_path, (x + 15, name_light_cone.size[1] - 26))
        holst.alpha_composite(icon_element, (x + 15 + icon_path.size[0] + 5, name_light_cone.size[1] - 26))
        
        return holst

    async def run(self):
        """
        Runs the process to create an image with character information and icons.
        
        :return: An image with character information and icons (PIL.Image.Image).
        """
        name_light_cone, icon_element, icon_path, max_level = await asyncio.gather(
            pill.create_image_text(self.character.name, 45, max_width=427, max_height=50, color=(255, 255, 255, 255)),
            pill.get_dowload_img(self.character.element.icon, thumbnail_size=(41, 41), cache=self.cache),
            pill.get_dowload_img(self.character.path.icon, size=(41, 41), cache=self.cache),
            self.get_max_lvl()
        )
        
        return await self.creat_holst(name_light_cone, icon_element, icon_path, max_level)

