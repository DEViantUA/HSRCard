# Copyright 2023 DEViantUa <t.me/deviant_ua>
# All rights reserved.
from PIL import Image
import threading
from weakref import WeakValueDictionary
from pathlib import Path

assets = Path(__file__).parent.parent / 'assets'
font = str(assets / 'font_hsr.ttf')

mapping = {
    
    'default': assets/'background'/'default.png',
    'default_maska': assets/'background'/'default_maska.png',
    'dark': assets/'background'/'dark.png',
    'frame_mask': assets/'background'/'frame_mask.png',
    'default_freme_line': assets/'background'/'default_freme_line.png',
    'adapt_freme_line': assets/'background'/'adapt_freme_line.png',
    
    'eidolon_open': assets/'eidolon'/'open.png',
    
    'eidolon_electro_open': assets/'eidolon'/'electro.png',
    'eidolon_fire_open': assets/'eidolon'/'fire.png',
    'eidolon_ice_open': assets/'eidolon'/'ice.png',
    'eidolon_imagunary_open': assets/'eidolon'/'imagunary.png',
    'eidolon_physikal_open': assets/'eidolon'/'physikal.png',
    'eidolon_quantom_open': assets/'eidolon'/'quantom.png',
    'eidolon_wind_open': assets/'eidolon'/'wind.png',
    
    'talants_background': assets/'talants'/'background.png',
    'default_frame': assets/'talants'/'default_frame.png',
    'adaptationt_frame': assets/'talants'/'adaptationt_frame.png',
    'count': assets/'talants'/'count.png',    
    
    'main_stats': assets/'talants'/'main_stats.png',
    'mini_stats': assets/'talants'/'mini_stats.png',
    'line_stats': assets/'talants'/'line.png',
    
    
    'background_up': assets/'relict'/'background_up.png',
    'frame_up': assets/'relict'/'frame_up.png',
    'background_centry': assets/'relict'/'background_centry.png',
    'frame_centry': assets/'relict'/'frame_centry.png',
    'background_down': assets/'relict'/'background_down.png',
    'frame_down': assets/'relict'/'frame_down.png',
    'relict_maska': assets/'relict'/'maska.png',
    'relict_line': assets/'relict'/'line.png',
    'count_level': assets/'relict'/'count_level.png',
    'sets_count': assets/'relict'/'sets_count.png',
    
    
    'shadow_3_light_cone': assets/'light_cones'/'3_shadow_lc.png',
    'star_3_frame_light_cone': assets/'light_cones'/'3_star_frame_lc.png',
    'shadow_4_light_cone': assets/'light_cones'/'4_shadow_lc.png',
    'star_4_frame_light_cone': assets/'light_cones'/'4_star_frame_lc.png',
    'shadow_5_light_cone': assets/'light_cones'/'5_shadow_lc.png',
    'star_5_frame_light_cone': assets/'light_cones'/'5_star_frame_lc.png',
    'blic_light_cones': assets/'light_cones'/'blic.png',
    'frame_light_cones': assets/'light_cones'/'frame_lc.png',
    'maska_light_cones': assets/'light_cones'/'maska_lc.png',
    'stats_light_cones': assets/'light_cones'/'stats.png',
    
    
    'stars_5': assets/'stars'/'stars_5.png',
    'stars_4': assets/'stars'/'stars_4.png',
    'stars_3': assets/'stars'/'stars_3.png',
    'stars_2': assets/'stars'/'stars_2.png',
    'stars_1': assets/'stars'/'stars_1.png',
    
    
}

class ImageCache:
    def __init__(self):
        self.mapping = mapping
        self.cache = WeakValueDictionary()
        self.lock = threading.Lock()
        self.assets = assets

    def __dir__(self):
        return sorted(set([*globals(), *self.mapping]))

    def __getattr__(self, name):
        path = self.mapping.get(name)
        if not path:
            raise AttributeError(name)
    
        with self.lock:
            try:
                image = self.cache[name]
            except KeyError:
                self.cache[name] = image = Image.open(self.assets / path)
        
            return image