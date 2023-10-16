# Copyright 2023 DEViantUa <t.me/deviant_ua>
# All rights reserved.

from PIL import Image
from ..tools import pill, openfile
import asyncio

_of = openfile.ImageCache()


class Eidolon:
    def __init__(self,eidolon,rank,element,cache) -> None:
        self.eidolon = eidolon
        self.cache = cache
        self.rank = rank
        self.element = element
        
    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass
    
    async def get_background_eidolon(self):
        if self.element == "Wind":
            return _of.eidolon_wind_open.copy()
        if self.element == "Fire":
            return _of.eidolon_fire_open.copy()
        if self.element == "Ice":
            return _of.eidolon_ice_open.copy()
        if self.element == "Thunder":
            return _of.eidolon_electro_open.copy()
        if self.element == "Quantum":
            return _of.eidolon_quantom_open.copy()
        if self.element == "Imaginary":
            return _of.eidolon_imagunary_open.copy()
        else:
            return _of.eidolon_physikal_open.copy()
    
    async def get_icon_open(self, icon):
        """
        Retrieves an icon for opening an eidolon with the specified icon image.
        
        :param icon: The icon image representing the eidolon to be opened.
        :return: An image with the eidolon opening icon (PIL.Image.Image).
        """
        background = await self.get_background_eidolon()#_of.eidolon_open.copy()
        icon = await pill.get_dowload_img(icon, size=(39, 39), cache=self.cache)
        background.alpha_composite(icon, (24, 24))
        
        return background

    
    async def get_icon_closed(self, icon):
        """
        Retrieves an icon for a closed eidolon with the specified icon image.
        
        :param icon: The icon image representing the closed eidolon.
        :return: An image with the closed eidolon icon (PIL.Image.Image).
        """
        background = Image.new("RGBA", (88, 88), (0, 0, 0, 0))
        icon = await pill.get_dowload_img(icon, size=(39, 39), cache=self.cache)
        icon = await pill.apply_opacity(icon, opacity=0.5)
        background.alpha_composite(icon, (24, 24))
        
        return background

        
    async def collect(self):
        """
        Collects and combines a list of icon images into a single image vertically.
        :return: A combined image with vertically stacked icons (PIL.Image.Image).
        """
        result = await asyncio.gather(*self.task)
        y = 0
        for icon in result:
            self.background.alpha_composite(icon, (0, y))
            y += 62

            
    async def run(self):
        """
        Runs the process to generate an image with open and closed eidolon icons.
        :return: An image with the combined icons (PIL.Image.Image).
        """
        self.background = Image.new("RGBA", (88, 402), (0, 0, 0, 0))
        self.task = []
        
        # Add open eidolon icons to the task list
        for key in self.eidolon[:self.rank]:
            self.task.append(self.get_icon_open(key))
        
        # Add closed eidolon icons to the task list
        for key in self.eidolon[self.rank:]:
            self.task.append(self.get_icon_closed(key))

        # Collect and combine the icons
        await self.collect()
        
        return self.background
