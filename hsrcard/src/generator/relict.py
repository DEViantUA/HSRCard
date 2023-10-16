
from PIL import Image,ImageFilter,ImageDraw
from ..tools import pill, openfile
import asyncio

_of = openfile.ImageCache()


class Relict:
    def __init__(self, relict, relic_sets, cache) -> None:
        """
        Initialize the Relict class with relict information, associated relic sets, and caching settings.

        :param relict: Information about the relict.
        :param relic_sets: Associated relic sets.
        :param cache: Caching settings for optimization.
        """
        self.relict = relict
        self.relic_sets = relic_sets
        self.cache = cache

        
    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass
    
    
    async def get_count_relict(self):
        """
        Count and return the number of relicts that end with digits 1, 2, 3, or 4.

        :return: The count of relicts ending with the specified digits.
        """
        count_relict = 0

        for key in self.relict:
            if str(key.id)[-1] in ["1", "2", "3", "4"]:
                count_relict += 1

        return count_relict - 1

    
    async def get_color_level(self, x):
        """
        Get and return a color based on the provided rarity level.

        :param x: The rarity level (e.g., 5 for 5-star rarity).
        :return: A color corresponding to the rarity level.
        """
        if x == 5:
            return (151, 117, 79)
        elif x == 4:
            return (116, 79, 151)
        elif x == 3:
            return (79, 132, 151)
        elif x == 2:
            return (79, 151, 118)
        else:
            return (255, 255, 255)

    
    async def get_open_resurs(self, type):
        """
        Get and return the open resource assets based on the provided type.

        :param type: The type of open resource (e.g., 1 for "up", 2 for "down", 3 for "centry").
        :return: A tuple containing the background and frame assets for the specified type.
        """
        if type == 1:
            return _of.background_up.copy(), _of.frame_up
        elif type == 2:
            return _of.background_down.copy(), _of.frame_down
        else:
            return _of.background_centry.copy(), _of.frame_centry

    async def get_stars(self,rarity):
        rank_names = [_of.stars_1,_of.stars_1, _of.stars_2, _of.stars_3, _of.stars_4, _of.stars_5]
        return rank_names[rarity] if 0 <= rarity <= 5 else _of.stars_1
        
    async def creat_relict(self,relict,type = 0):
        """
        Create and return an image representing a relict with its associated attributes and affixes.

        :param relict: Information about the relict.
        :param type: The type of relict (0 for general, 1 for "up", 2 for "down", 3 for "centry").
        :return: A dictionary containing the relict image mapped by its last digit in the ID.
        """
        
        background,frame_background  = await self.get_open_resurs(type)
        
        holst = Image.new("RGBA", (486,102), (0,0,0,0))
        holst_relict = Image.new("RGBA", (486,102), (0,0,0,0))
        icon_relict = await pill.get_dowload_img(relict.icon, size=(120, 120), cache= self.cache)
        
        holst_relict.alpha_composite(icon_relict,(-6,-10))

        holst.paste(holst_relict,(0,0,),_of.relict_maska.convert("L"))
        
        background.alpha_composite(holst)
        background.alpha_composite(_of.relict_line)
        count_level_background = _of.count_level.copy()
        
        icon = await pill.get_dowload_img(relict.main_affix.icon, size=(56, 56))
        display = relict.main_affix.display
        level = f"+{relict.level}"

        
        font = await pill.get_font(20)
        d = ImageDraw.Draw(count_level_background)
        x = int(font.getlength(level)/2)
        d.text((26 - x, 1), str(level), font=font, fill=(160,137,86,255))
        
        background.alpha_composite(icon,(95,0))
        background.alpha_composite(count_level_background,(48,17))
        
        d = ImageDraw.Draw(background)
        x = int(font.getlength(display))
        d.text((139 - x, 63), str(display), font=font, fill=(255,255,255, 255))
        
        position = (
            (171,0),
            (320,0),
            (171,44),
            (320,44)
        )
        font = await pill.get_font(24)
        for i, k in enumerate(relict.sub_affix):
            icon = await pill.get_dowload_img(k.icon, size=(50, 50))
            background.alpha_composite(icon,position[i])
            d.text((position[i][0]+49, position[i][1]+15), str(k.display), font=font, fill=(255,255,255, 255))
        
        holst = Image.new("RGBA", (491,102), (0,0,0,0))
        
        holst.alpha_composite(background,(5,0))
        
        color = await self.get_color_level(relict.rarity)
        stars = await self.get_stars(relict.rarity)
        holst.alpha_composite(stars.copy().resize((26,84)),(2,18))
        
        frame_background = await pill.recolor_image(frame_background,color)
        holst.alpha_composite(frame_background)
        
        return {str(relict.id)[-1:]: {"holst": holst, "type": type}}
    
    async def get_sets(self):
        """
        Retrieve information about relic sets, including their IDs, names, icons, and optional properties.

        :return: A dictionary mapping relic set IDs to their corresponding information.
        """
        rel_set = {}
        for key in self.relic_sets:
            if key.id not in rel_set:
                if key.properties == []:
                    rel_set[key.id] = {"num": int(key.num), "name": key.name, "icon": key.icon, "properties": None}
                else:
                    rel_set[key.id] = {"num": int(key.num), "name": key.name, "icon": key.icon, "properties": {"icon": key.properties[0].icon, "display": key.properties[0].display}}
            else:
                rel_set[key.id]["num"] = int(key.num)

        return rel_set

    
    async def creat_sets(self):
        """
        Creates a set of images representing sets with related information and returns a composite image.

        :return: A composite image containing information about sets (Image.Image).
        """
        hols = Image.new("RGBA", (488,100), (0,0,0,0))

        rel_set = await self.get_sets()
        
        font = await pill.get_font(18)
        
        line_items = []
        
        for key in rel_set:
            sets = rel_set[key]
            holst_line = Image.new("RGBA", (488,26), (0,0,0,0))
            background_count = _of.sets_count.copy()
            d = ImageDraw.Draw(background_count)
            d.text((12, 3), str(sets["num"]), font=font, fill=(222, 196, 131, 255))
            d = ImageDraw.Draw(holst_line)
            sets_name_font,size = await pill.get_text_size_frame(sets["name"],18,446)
            if key[:1] == "1":
                holst_line.alpha_composite(background_count)
                d.text((int(41), 3), sets["name"], font=sets_name_font, fill=(222, 196, 131, 255))
                line_items.append({"setap": 0, "line": holst_line})
            else:
                holst_line.alpha_composite(background_count,(453,0))
                d.text((int(447-size), 3), sets["name"], font=sets_name_font, fill=(222, 196, 131, 255))
           
                line_items.append({"setap": 1, "line": holst_line})
        
        y = 0
        for key in line_items:
            if key["setap"] == 1:
                hols.alpha_composite(key["line"],(0,66))
            else:
                hols.alpha_composite(key["line"],(0,y))
                y += 33
            
        
        return hols
    
    async def run(self):
        """
        Executes a series of asynchronous tasks to gather information about relics and sets,
        and returns a dictionary containing the gathered data.

        :return: A dictionary with information about relics and sets, including images (dict).
        """
        count_relict = await self.get_count_relict()
        
        task = []
        i = 0
        for _,key in enumerate(self.relict):
            if str(key.id)[-1:] in ["1","2","3","4"]:
                if _ == 0:
                    task.append(self.creat_relict(key,type=1))
                elif _ == count_relict:
                    task.append(self.creat_relict(key,type=2))
                else:
                    task.append(self.creat_relict(key))
            else:
                if i == 0:
                    task.append(self.creat_relict(key,type=1))
                else:
                    task.append(self.creat_relict(key,type=2))
                i += 1
            

        sets = await self.creat_sets()
        results = await asyncio.gather(*task) 
        
        relict = {}  
        for res in results:
            relict.update(res) 
                
        return {"relict": relict, "sets": sets}
