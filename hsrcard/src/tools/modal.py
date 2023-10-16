# Copyright 2023 DEViantUa <t.me/deviant_ua>
# All rights reserved.

from pydantic import BaseModel
from typing import List ,Optional,Union

from PIL import Image

class Avatar(BaseModel):
    id: Optional[str]
    name: Optional[str]
    icon: Optional[str]
    
class PlayerV2(BaseModel):
    uid: Optional[str]
    nickname: Optional[str]
    level: Optional[int]
    avatar: Avatar
    signature: Optional[str]
    friend_count: Optional[int]
    world_level: Optional[int]

class Card(BaseModel):
    id: Optional[str]
    name: Optional[str]
    rarity: Optional[int]
    card: Image.Image
    class Config:
        arbitrary_types_allowed = True
    size: Optional[tuple]
    
class Settings(BaseModel):
    uid: Optional[int]
    lang: Optional[str]
    hide: Optional[bool]
    save: Optional[bool]
    background: Optional[bool]

class HSRCard(BaseModel):
    settings: Settings
    player: PlayerV2
    card: Optional[Union[List[Card], Image.Image]] 
    name: Optional[str]
    id: Optional[str]
    class Config:
        arbitrary_types_allowed = True