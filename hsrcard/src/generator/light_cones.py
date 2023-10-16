# Copyright 2023 DEViantUa <t.me/deviant_ua>
# All rights reserved.

from PIL import Image, ImageDraw
from ..tools import pill, openfile

_of = openfile.ImageCache()


class LightCones:
    def __init__(self, light_cone, cache, lang) -> None:
        """
        Initializes a LightCones object with information about light cones, cache, and language settings.
        
        :param light_cone: Information about the light cones.
        :param cache: A cache for storing data.
        :param lang: Language settings and translations.
        """
        self.light_cone = light_cone
        self.cache = cache
        self.lang = lang

    async def get_ranks(self):
        """
        Get the rank name for a given light cone's rank.

        :return: The rank name (e.g., "O", "I", "II", ...) or "O" if the rank is out of range.
        """
        rank_names = ["O", "I", "II", "III", "IV", "V"]
        return rank_names[self.light_cone.rank] if 0 <= self.light_cone.rank <= 5 else "O"
    
    async def get_stars(self):
        rank_names = [_of.stars_1,_of.stars_1, _of.stars_2, _of.stars_3, _of.stars_4, _of.stars_5]
        return rank_names[self.light_cone.rarity] if 0 <= self.light_cone.rarity <= 5 else _of.stars_1
    
    async def get_max_lvl(self):
        """
        Get the maximum character level based on the promotion level of the light cone.
        
        :return: The maximum character level (e.g., 20, 30, ...) or 80 if the promotion level is out of range.
        """
        max_levels = [20, 30, 40, 50, 60, 70, 80]
        return max_levels[self.light_cone.promotion] if 0 <= self.light_cone.promotion <= 6 else 80
    
    async def get_resurs_light_cones(self, x):
        """
        Get resources (shadow image, frame image, and color) for a specific light cone level.
        
        :param x: The light cone level (e.g., 3, 4, 5).
        :return: A tuple of shadow image, frame image, and color, or (None, None, (0, 0, 0, 0)) if the level is not found.
        """
        resources = {
            3: (_of.shadow_3_light_cone, _of.star_3_frame_light_cone, (150, 202, 255, 255)),
            4: (_of.shadow_4_light_cone, _of.star_4_frame_light_cone, (217, 150, 255, 255)),
            5: (_of.shadow_5_light_cone, _of.star_5_frame_light_cone, (255, 199, 150, 255))
        }
        return resources.get(x, (None, None, (0, 0, 0, 0)))

    async def creat_lc_icon(self):
        """
        Creates an image for a light cone icon, combining portrait, frame, shadow, and other elements.
        
        :return: An image of the light cone icon (PIL.Image.Image).
        """
        light_cone_holst = Image.new("RGBA", (337, 448), (0, 0, 0, 0))
        light_cone_holst_image = Image.new("RGBA", (337, 448), (0, 0, 0, 0))

        image = await pill.get_dowload_img(self.light_cone.portrait, size=(298, 410))
        light_cone_holst_image.alpha_composite(image, (19, 23))

        light_cone_holst.paste(light_cone_holst_image, (0, 0), _of.maska_light_cones.convert("L"))

        light_cone_holst_image = Image.new("RGBA", (337, 448), (0, 0, 0, 0))
        shadow, frame, self.color = await self.get_resurs_light_cones(self.light_cone.rarity)
        light_cone_holst_image.alpha_composite(shadow, (0, 0))
        light_cone_holst_image.alpha_composite(frame, (32, 29))
        light_cone_holst_image.alpha_composite(light_cone_holst, (0, 0))
        light_cone_holst_image.alpha_composite(_of.frame_light_cones, (0, 0))
        light_cone_holst_image.alpha_composite(_of.blic_light_cones, (0, 0))
        light_cone_holst_image.alpha_composite(frame, (0, 0))

        return light_cone_holst_image

    async def creat_stats_info(self):
        """
        Creates an image for light cone stats information, including rank, level, and attributes.
        
        :return: An image with light cone stats information (PIL.Image.Image).
        """
        background = _of.stats_light_cones.copy()
        font_size = 29
        font_color = (193, 162, 103, 255)

        font = await pill.get_font(font_size)

        d = ImageDraw.Draw(background)
        rank = await self.get_ranks()
        x = int(font.getlength(rank) / 2)
        d.text((205 - x, 130), rank, font=font, fill=font_color)

        font = await pill.get_font(19)

        max_level = await self.get_max_lvl()

        d.text((226,134), f"{self.lang.lvl}: {self.light_cone.level}/{max_level}", font=font, fill=(255, 255, 255, 255))
        
        d.text((238, 180), self.light_cone.attributes[0].display, font=font, fill=(255, 255, 255, 255)) #HP
        d.text((341, 180), self.light_cone.attributes[1].display, font=font, fill=(255, 255, 255, 255)) #ATK
        d.text((238, 226), self.light_cone.attributes[2].display, font=font, fill=(255, 255, 255, 255)) #DEF
        
        return background

    async def run(self):
        """
        Runs the process to create an image for a light cone, including its icon, name, rank, and stats information.
        
        :return: An image with light cone information (PIL.Image.Image).
        """
        if self.light_cone is None:
            return Image.new("RGBA", (0, 0), (0, 0, 0, 0))

        icon_light_cone = await self.creat_lc_icon()
        icon_light_cone = icon_light_cone.resize((183, 244))
        stars = await self.get_stars()
        name_light_cone = await pill.create_image_with_text(self.light_cone.name, 24, max_width=230, color=(255, 255, 255, 255))
        line = Image.new("RGBA", (1, name_light_cone.size[1] + 2), self.color)
        frame_stats = await self.creat_stats_info()

        background = Image.new("RGBA", (447, 255), (0, 0, 0, 0))
        background.alpha_composite(icon_light_cone)
        background.alpha_composite(stars,(0,6))
        background.alpha_composite(line, (191, 19))
        background.alpha_composite(name_light_cone, (200, 23))

        if line.size[1] > 50:
            y = int(0 - line.size[1] / 2)
        else:
            y = -45

        background.alpha_composite(frame_stats, (0, y))

        return background
