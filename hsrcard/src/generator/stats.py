# Copyright 2023 DEViantUa <t.me/deviant_ua>
# All rights reserved.

from PIL import Image,ImageDraw
from ..tools import pill
import asyncio

class Stats:
    def __init__(self, stats, cache) -> None:
        """
        Initialize the Stats class with stats data and caching settings.

        :param stats: The stats data to be displayed.
        :param cache: Caching settings to optimize image retrieval.
        """
        self.stats = stats
        self.cache = cache
        self.position = 0
        self.position_line = 0
        self.holst = Image.new("RGBA", (397, 720), (0, 0, 0, 0))
        
    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass
    
    async def get_dop_stats(self):
        """
        Get additional (dop) stats by combining and summing attributes with the same field.
        
        :return: A tuple containing additional stats dictionary, combined attributes dictionary, and the number of unique fields.
        """
        combined_attributes = {}
        dop = {}
        for attribute in self.stats:
            field = attribute.field
            if field in combined_attributes:
                combined_attributes[field].value += attribute.value
                dop[field]["dop"] = f"+{attribute.display}"
            else:
                dop[field] = {"main": attribute.display, "dop": 0}
                combined_attributes[field] = attribute
        return {key: value for key, value in dop.items() if value['dop'] != 0}, combined_attributes, len(dop)

    async def count_attributes(self,attributes):
        """
        Count the number of attributes in the given dictionary.
        
        :param attributes: A dictionary of attributes.
        :return: The number of attributes in the dictionary.
        """
        count = 0
        for key, value in attributes.items():
            count += 1
        return count
    
    async def calculate_vertical_spacing(self):
        """
        Calculate the vertical spacing between lines based on the number of lines.

        :return: The vertical spacing value as an integer.
        """
        if self.len_line <= 1:
            return 0
        x = 670 / (self.len_line - 1)
        return int(x)
    
    async def creat_stats_dop(self,attribute):
        """
        Create and position additional (dop) stats text on the stats line.
        
        :param attribute: The attribute field to which the dop stats belong.
        """
        x = 396 - int(self.font.getlength(str(self.value)))
        self.draw_stats_line.text((x, self.position+5), str(self.value), font=self.font, fill=(255, 255, 255, 255))
        x = 396 - int(self.font_dop.getlength(self.dop[attribute]["dop"]))
        self.draw_stats_line.text((x, self.position+34), self.dop[attribute]["dop"], font=self.font_dop, fill=(229, 195, 144, 255))
        x = x - int(self.font_dop.getlength(self.dop[attribute]["main"])) - 5
        self.draw_stats_line.text((x, self.position+34), self.dop[attribute]["main"], font=self.font_dop, fill=(255, 255, 255, 255))
    
    async def creat_stats(self):
        """
        Create and position the primary (main) stats text on the stats line.
        """
        x = 396 - int(self.font.getlength(str(self.value)))
        self.draw_stats_line.text((x, self.position+15), str(self.value), font=self.font, fill=(255, 255, 255, 255))
        
    async def get_font_stats(self):
        """
        Get and store fonts for both main and additional (dop) stats text.
        
        :return: A tuple containing the main stats font and the dop stats font.
        """
        self.font, self.font_dop = await asyncio.gather(pill.get_font(24), pill.get_font(15))
        return self.font, self.font_dop
    
    async def get_stats_line(self,attribute):
        """
        Get and assemble a stats line, including the icon, attribute name, and either main or additional (dop) stats.

        :param attribute: The attribute field.
        :return: A tuple containing the assembled stats line image and the attribute name text image.
        """

        icon = await pill.get_dowload_img(self.stat.icon, size=(50,50))

        self.draw_stats_line = ImageDraw.Draw(self.line_stat_holst)
        self.line_stat_holst.alpha_composite(icon, (0,self.position))
        self.name_text = await pill.create_image_text(self.stat.name, 24, max_width=180, max_height=35, color=(255, 255, 255, 255))
        
        if self.name_text.size[1] < 45:
            self.line_stat_holst.alpha_composite(self.name_text, (58,self.position+15))
        else:
            self.line_stat_holst.alpha_composite(self.name_text, (58,self.position))
            
        if attribute in self.dop:
           await self.creat_stats_dop(attribute)
        else:
            await self.creat_stats()
        
        return self.line_stat_holst,self.name_text
    
    async def add_line(self):
        """
        Add a separating line to the stats line image.
        
        :return: The stats line image with the added separating line.
        """
        line = Image.new("RGBA", (397-int(self.font.getlength(str(self.value)))-72-self.name_text.size[0],2), (255,255,255,100))
        self.line_stat_holst.alpha_composite(line,(self.name_text.size[0]+58+5,self.position+27))
        
        return self.line_stat_holst
        
    async def run(self):
        """
        Generate a holst image containing a list of stats lines with main and additional (dop) attributes.
        
        :return: The holst image with stats lines.
        """
        self.dop, self.combined_attributes, self.len_line = await self.get_dop_stats()
        await self.get_font_stats()

        position_line_add = await self.calculate_vertical_spacing()
                    
        for attribute in self.combined_attributes:
            self.line_stat_holst = Image.new("RGBA", (397, 50), (0, 0, 0, 0))
            self.stat = self.combined_attributes[attribute]
            self.value = "{:.1f}%".format(self.stat.value * 100) if self.stat.percent else round(self.stat.value)
                
            await self.get_stats_line(attribute)
            await self.add_line()

            self.holst.alpha_composite(self.line_stat_holst, (0, self.position_line))
            self.position_line += position_line_add

        return self.holst
