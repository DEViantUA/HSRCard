# Copyright 2023 DEViantUa <t.me/deviant_ua>
# All rights reserved.

from .src.tools import translation, pill, modal
from .src.generator import card
from honkairail import starrailapi
import asyncio,re,os,datetime

def process_input(characterImgs, characterName):
    if characterImgs:
        if isinstance(characterImgs, dict):
            characterImgs = {key.lower(): value for key, value in characterImgs.items()}
        else:
            raise TypeError("The charterImg parameter must be a dictionary, where the key is the name of the character, and the parameter is an image.\nExample: charterImg = {'Himeko': 'img.png'} or {'Himeko': 'img.png', 'Seele': 'img2.jpg', ...}")

    if characterName:
        if isinstance(characterName, str):
            characterName = [name.strip().lower() for name in characterName.split(",")]
        else:
            raise TypeError("The name parameter must be a string, to pass multiple names, list them separated by commas.\nExample: name = 'Himeko' or name = 'Himeko, Seele',..")
    
    return characterImgs, characterName


def remove_html_tags(text):
    clean_text = re.sub('<.*?>', '', text)
    return clean_text

class HonkaiCard():
    def __init__(self,lang = "en", characterImgs = None, characterName = None, hide = False, save = False, cache = True):
        if not lang in translation.supportLang:
            self.lang = "en"
        else:
            self.lang = lang
        
        self.translateLang = translation.Translator(lang)
        
        try:
            self.characterImgs, self.characterName = process_input(characterImgs, characterName)
        except Exception as e:
            print(e.message)
            return

        self.API = starrailapi.StarRailApi(lang, v = 2)
        self.save = save
        self.hide = hide
        self.img = None
        self.cache = cache
        self.name = ""
        self.id = ""
        self.card = None
        
    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass
    
    async def saveBanner(self,res, name):
        data = datetime.datetime.now().strftime("%d_%m_%Y %H_%M")
        path = os.path.join(os.getcwd(), "RailCard", str(self.uid))
        os.makedirs(path, exist_ok=True)
        file_path = os.path.join(path, f"{name}_{data}.png")
        res.save(file_path)
    
    async def characterImg(self,name,ids):
        if name in self.characterImgs:
            self.img = await pill.get_user_image(self.characterImgs[name], cache = self.cache)
        else:
            self.img = None
        
        if ids in self.characterImgs:
            self.img = await pill.get_user_image(self.characterImgs[ids], cache = self.cache)
        
    async def collect_data(self):
        user = {
            "settings": {
                "uid": int(self.uid),
                "lang": self.lang,
                "hide": self.hide,
                "save": self.save,
            },
            "player": self.data.player,
            "card": self.card,
            "name": self.name,
            "id": self.id,
        }
        
        return modal.HSRCard(**user) 
    
    async def creat(self, uid):
        task = []
        self.uid = uid 
        self.data = await self.API.get_full_data(self.uid)

        for key in self.data.characters:
            
            self.name += f"{key.name}, "
            self.id += f"{key.id}, "
            
            if self.characterName:
                if not key.name.lower() in self.characterName and not str(key.id) in self.characterName:
                    continue       

            if self.characterImgs:
                await self.characterImg(key.name.lower(), str(key.id))
            task.append(card.Creat(key, self.translateLang,self.img,self.hide,int(uid),self.cache).start())
            
        self.card = await asyncio.gather(*task)
        
        if self.save:
            for keys in self.card:
                await self.saveBanner(keys["card"], keys["name"])
        
        return await self.collect_data()