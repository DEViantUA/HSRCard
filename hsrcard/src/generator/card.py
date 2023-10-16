# Copyright 2023 DEViantUa <t.me/deviant_ua>
# All rights reserved.

from . import background, eidolon, info, light_cones, relict, stats, skill
import asyncio

class Creat:
    def __init__(self, characters,lang,img,hide,uid,cache) -> None:
        self.character = characters
        self.lang = lang
        self.img = img
        self.hide = hide
        self.uid = uid
        self.cache = cache
        self.relict_position = {
            "1": (1425, 21),
            "2": (1425, 132),
            "3": (1425, 246),
            "4": (1425, 357),
            "5": (1425, 579),
            "6": (1425, 690),
        }

        self.relict_positions = [
            (1425, 21),
            (1425, 132),
            (1425, 246),
            (1425, 357),
            (1425, 579),
            (1425, 690),
        ]
    
    async def start(self):
        tasks = [
            background.Background(self.character, self.img, self.cache, self.uid, self.hide).run(),
            eidolon.Eidolon(self.character.rank_icons, self.character.rank, self.character.element.id,self.cache).run(),
            skill.Skill(self.character.skill_trees, self.cache, self.character.element.id, self.character.path.id).run(),
            light_cones.LightCones(self.character.light_cone, self.cache, self.lang).run(),
            info.Info(self.character, self.cache, self.lang).run(),
            stats.Stats(self.character.attributes + self.character.additions, self.cache).run(),
            relict.Relict(self.character.relics, self.character.relic_sets, self.cache).run()
        ]

        background_card, eidolon_card, skill_card, light_cone_card, info_card, stats_card, relict_card = await asyncio.gather(*tasks)

        background_card.alpha_composite(eidolon_card, (389, 29))
        background_card.alpha_composite(skill_card, (483, 174))
        background_card.alpha_composite(light_cone_card, (477, 509))
        background_card.alpha_composite(info_card, (494, 44))
        background_card.alpha_composite(stats_card, (948, 49))

        i = 0
        x = 4
        for key in relict_card["relict"]:
            if key in ["5","6"]:
                background_card.alpha_composite(relict_card["relict"][key]["holst"], self.relict_positions[x]) 
                x += 1
            else:
                background_card.alpha_composite(relict_card["relict"][key]["holst"], self.relict_positions[i])      
                i += 1          

        background_card.alpha_composite(relict_card["sets"], (1425, 469))
            
            
        data = {
            "id": self.character.id,
            "name": self.character.name,
            "rarity": self.character.rarity,
            "card": background_card,
            "size": background_card.size
        }
        
        return data