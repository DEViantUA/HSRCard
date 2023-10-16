# Copyright 2023 DEViantUa <t.me/deviant_ua>
# All rights reserved.

from PIL import Image,ImageDraw
from ..tools import pill, openfile
import asyncio

_of = openfile.ImageCache()


tree = {
    "Rogue":{
        "01": (89,12),
        "02": (89,85),"03": (152,85),"04": (215,85),
        "05": (215,159),"06": (152,159),"07": (89,159),
        "08": (89,233),"09": (152,233),"10": (215,233)
    },

    "Knight": {
        "01": (89,12),
        "02": (89,85),"03": (152,85),"04": (215,85),
        "05": (215,159),"06": (152,159),"07": (89,159),
        "08": (89,233),"09": (152,233),"10": (215,233),
    },

    "Warrior": {
        "01": (89,12),
        "02": (89,85),"03": (152,85),"04": (215,85),
        "05": (215,159),"06": (152,159),"07": (89,159),
        "08": (89,233),"09": (152,233),"10": (215,233),
    },

    "Priest": {
        "01": (89,12),"10": (152,12),
        "02": (89,85),"03": (152,85),"04": (215,85),
        "05": (215,159),"06": (152,159),"07": (89,159),
        "08": (89,233),"09": (152,233)
    },

    "Warlock": {
        "01": (89,12),"10": (152,12),
        "02": (89,85),"03": (152,85),"04": (215,85),
        "05": (215,159),"06": (152,159),"07": (89,159),
        "08": (89,233),"09": (152,233)
    },

    "Mage": {
        "01": (89,12),"10": (152,12),
        "02": (89,85),"03": (152,85),"04": (215,85),
        "05": (215,159),"06": (152,159),"07": (89,159),
        "08": (89,233),"09": (152,233)
    },

    "Shaman":{
        "01": (152,12),"04": (152,12),"07": (215,12),
        "02": (89,85),"03": (152,85),"05": (89,159),"06": (152,159),
        "08": (89,233),"09": (152,233),"10": (215,233)
    }
}

position_point = {
    "Point05": (0, 0),
    "Point06": (0, 73),
    "Point07": (0, 146),
    "Point08": (0, 219),
}

class Skill:
    def __init__(self, skill, cache, element, path) -> None:
        """
        Initializes a Talents object with Skill information, cache, element, and file path.
        
        :param skill: Information about the skill or talent.
        :param cache: A cache for storing data.
        :param element: The element associated with the skill.
        :param path: The file path related to the skill.
        """
        self.skill = skill
        self.cache = cache
        self.element = element
        self.path = path

    
    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass
       
    async def get_color_level(self, max_level):
        """
        Returns a color level based on the provided maximum level and element type.
        
        :param max_level: The maximum level for which the color is determined.
        :return: A tuple representing the RGBA color value.
        """
        if max_level > 10:
            if self.element == "Wind":
                return (110, 255, 158, 255)
            if self.element == "Fire":
                return (255, 110, 110, 255)
            if self.element == "Ice":
                return (110, 202, 255, 255)
            if self.element == "Thunder":
                return (192, 110, 255, 255)
            if self.element == "Quantum":
                return (110, 113, 255, 255)
            if self.element == "Imaginary":
                return (255, 223, 110, 255)
            else:
                return (255, 255, 255, 255)
        else:
            return (227, 215, 194, 255)
   
    async def creat_count(self, level, max_level):
        """
        Creates a count display with a specified level and color based on the maximum level.
        
        :param level: The level to display.
        :param max_level: The maximum level used for determining the color.
        :return: An image with the count display (PIL.Image.Image).
        """
        color, font = await asyncio.gather(self.get_color_level(max_level), pill.get_font(24))
        
        background = _of.count.copy()
        
        d = ImageDraw.Draw(background)
        x = int(font.getlength(str(level)) / 2)
        d.text((15 - x, 4), str(level), font=font, fill=color)
        
        return background

    async def creat_main_skill(self, icon):
        """
        Creates a main skill display with the specified icon.
        
        :param icon: The icon image representing the main skill.
        :return: An image with the main skill display (PIL.Image.Image).
        """
        background = _of.talants_background.copy()
        icon = await pill.get_dowload_img(icon, size=(55, 55), cache=self.cache)
        icon = await pill.recolor_image(icon, (227, 215, 194))
        background.alpha_composite(icon, (4, 4))
        
        return background

    async def add_frame(self, max_level):
        """
        Adds a frame with a color based on the provided maximum level.
        
        :param max_level: The maximum level used to determine the frame color.
        :return: An image with the colored frame (PIL.Image.Image).
        """
        color = await self.get_color_level(max_level)
        frame = _of.adaptationt_frame.copy()
        frame = await pill.recolor_image(frame, (color[0], color[1], color[2]))
        return frame

    async def get_main_skill_icon(self, skill):
        """
        Retrieves the main skill icon with associated information.
        
        :param skill: The skill information (including icon, level, and max level).
        :return: An image representing the main skill icon with details (PIL.Image.Image).
        """
        holst = Image.new("RGBA", (69, 68), (0, 0, 0, 0))
        background, count, frame = await asyncio.gather(self.creat_main_skill(skill.icon),self.creat_count(skill.level, skill.max_level),self.add_frame(skill.max_level))                                           
        background.alpha_composite(frame)
        holst.alpha_composite(background, (5, 0))
        holst.alpha_composite(count, (0, 37))
        
        return holst

    async def get_dop_skill_icon(self, icon, level):
        """
        Retrieves an additional skill icon with the specified icon and level.
        
        :param icon: The icon image representing the additional skill.
        :param level: The level of the additional skill.
        :return: An image representing the additional skill icon (PIL.Image.Image).
        """
        background = _of.main_stats.copy()
        icon = await pill.get_dowload_img(icon, size=(40, 40), cache=self.cache)
        icon = await pill.recolor_image(icon, (0, 0, 0))
        background.alpha_composite(icon, (13, 14))
        if level == 0:
            background = await pill.apply_opacity(background, opacity=0.5)
        
        return background
       
    async def creat_dop_mini_skill_icon(self, icon, level):
        """
        Creates a mini additional skill icon with the specified icon and level.
        
        :param icon: The icon image representing the additional skill.
        :param level: The level of the additional skill.
        :return: An image representing the mini additional skill icon (PIL.Image.Image).
        """
        background = _of.mini_stats.copy()
        icon = await pill.get_dowload_img(icon, size=(40, 40), cache=self.cache)
        icon = await pill.recolor_image(icon, (0, 0, 0))
        background.alpha_composite(icon, (0, 0))
        if level == 0:
            background = await pill.apply_opacity(background, opacity=0.5)
        
        return background
  
    async def collect(self):
        """
        Collects and combines two images (holst_main and holst_dop) into a single image.
        :return: The combined image (PIL.Image.Image).
        """
        holst = Image.new("RGBA", (345, 296), (0, 0, 0, 0))
        holst.alpha_composite(self.holst_main, (0, 0))
        holst.alpha_composite(self.holst_dop, (80, 6))
        
        return holst
  
    async def run(self):
        """
        Runs the talent generation process, creating images for main and additional skills.
        
        :return: A combined image of main and additional skills (PIL.Image.Image).
        """
        self.holst_main = Image.new("RGBA", (69, 296), (0, 0, 0, 0))
        self.holst_dop = Image.new("RGBA", (265, 293), (0, 0, 0, 0))
        line = _of.line_stats.convert("RGBA")
        position_dop = tree.get(self.path)
        position_main_y = 0
        
        for key in self.skill:
            if key.max_level != 1:
                icon_skill = await self.get_main_skill_icon(key)
                self.holst_main.alpha_composite(icon_skill, (0, position_main_y))
                position_main_y += 76
            else:
                if key.anchor in ["Point05", "Point06", "Point07", "Point08"]:
                    icon = await self.get_dop_skill_icon(key.icon, key.level)
                    self.holst_dop.alpha_composite(icon, position_point[key.anchor])
                else:
                    icon = await self.creat_dop_mini_skill_icon(key.icon, key.level)
                    self.holst_dop.alpha_composite(icon, position_dop[str(key.id)[-2:]])
                    self.holst_dop.alpha_composite(line, (position_dop[str(key.id)[-2:]][0] - 18, position_dop[str(key.id)[-2:]][1] + 21))
        
        return await self.collect()

