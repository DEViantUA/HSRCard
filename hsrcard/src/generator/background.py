# Copyright 2023 DEViantUa <t.me/deviant_ua>
# All rights reserved.

from PIL import Image,ImageFilter,ImageDraw
from ..tools import pill, openfile


_of = openfile.ImageCache()


class Background:
    def __init__(self, character, img, cache, uid, hide) -> None:
        """
        Initializes a Background object with character information, image, cache, UID, and hide status.
        
        :param character: Information about the character (e.g., character.portrait).
        :param img: An image associated with the background.
        :param cache: A cache for storing data.
        :param uid: The User ID (UID).
        :param hide: A flag indicating whether to hide certain elements.
        """
        self.character = character
        self.img = img
        self.cache = cache
        self.hide = hide
        self.uid = uid

        
    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass
    
    async def get_user_background(self):
        """
        Gets the user-defined background for the image.
        :return: A tuple of two images - one with opacity and one without (PIL.Image.Image).
        """
        userImages = await pill.get_centr_honkai_art((684, 814), self.img)
        grandient = await pill.GradientGenerator(userImages).generate(1, 813)
        background = grandient.resize((1950, 813)).convert("RGBA")
        
        background_opacity = background.copy()
        userImages_opacity = await pill.apply_opacity(userImages.copy(), opacity=0.6)
        background_opacity.alpha_composite(userImages_opacity,(-158,0))
        background.alpha_composite(userImages,(-158,0))
        
        return background_opacity, background



    async def get_splash_background(self):
        """
        Retrieves the splash background image.
        :return: A tuple of two images - one with opacity and one without (PIL.Image.Image).
        """
        splash = await pill.get_dowload_img(link=self.character.portrait, cache=self.cache)
        splash = await pill.get_centr_honkai((684, 813), splash)
        splash_opacity = await pill.apply_opacity(splash.copy(), opacity=0.5)
        
        background_opacity = _of.default.copy()
        background_opacity.alpha_composite(splash_opacity,(-158,0))
        background = _of.default.copy()
        background.alpha_composite(splash,(-158,0))
        
        return background_opacity, background

        
    async def get_blur_background(self, radius=20):
        """
        Blurs the image using a Gaussian filter with the specified radius.
        :param radius: Радиус размытия (по умолчанию 28).
        :return: Размытое изображение (Image.Image).
        """
        blurred_image = self.background_opacity.filter(ImageFilter.GaussianBlur(radius))
        return blurred_image

    async def get_frame_background(self):
        """
        Generates a frame background image.
        :return: A frame background image (PIL.Image.Image).
        """
        holst = Image.new("RGBA", (1950, 813), (0, 0, 0, 0))
        blurred_image = await self.get_blur_background()
        holst.paste(blurred_image, (0, 0), _of.frame_mask.convert("L"))
        
        return holst


    async def get_background(self):
        """
        Retrieves the background image.
        :return: A background image (PIL.Image.Image).
        """
        holst_background = Image.new("RGBA", (1950, 813), (0, 0, 0, 0))
        holst_background.paste(self.background, (0, 0), _of.default_maska.convert("L"))
        
        return holst_background

    
    async def add_frame(self, holst, adapt=False):
        """
        Adds a frame to the given image.
        :param holst: The image to which the frame is added (PIL.Image.Image).
        :param adapt: Whether to adapt the frame using soft light blending (boolean).
        :return: The image with the frame added (PIL.Image.Image).
        """
        if adapt:
            holst = await pill.apply_soft_light(holst, _of.adapt_freme_line)
        else:
            holst.alpha_composite(_of.default_freme_line)
        
        return holst

    
    async def add_uid(self, holst_background):
        """
        Adds a UID (User ID) to the background image.
        :param holst_background: The background image to which the UID is added (PIL.Image.Image).
        :return: The image with the UID added (PIL.Image.Image).
        """
        if self.hide:
            return holst_background
        else:
            holst_uid = Image.new("RGBA", (151, 21), (0, 0, 0, 0))
            font = await pill.get_font(18)
            d = ImageDraw.Draw(holst_uid)
            d.text((4, 3), f"UID:{self.uid}", font=font, fill=(0, 0, 0, 100))
            d.text((5, 3), f"UID:{self.uid}", font=font, fill=(255, 255, 255, 200))
            holst_background.alpha_composite(holst_uid, (15, 775))
        
        return holst_background

            
    async def run(self):
        """
        Performs the image processing workflow.
        :return: The final processed image (PIL.Image.Image).
        """
        if self.img:
            self.background_opacity, self.background = await self.get_user_background()
        else:
            self.background_opacity, self.background = await self.get_splash_background()

        holst = await self.get_frame_background()
        holst_background = await self.get_background()

        if self.img:
            holst = await self.add_frame(holst, adapt=True)
        else:
            holst = await self.add_frame(holst)

        holst_background.alpha_composite(holst)

        holst_background.alpha_composite(_of.dark)

        holst_background = await self.add_uid(holst_background)

        return holst_background