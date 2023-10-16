# Copyright 2023 DEViantUa <t.me/deviant_ua>
# All rights reserved.
from PIL import ImageFont,Image,ImageChops,ImageStat,ImageDraw
from io import BytesIO
from . import openfile
import aiohttp,re, json
from cachetools import TTLCache


async def get_font(size):
    return ImageFont.truetype(openfile.font, size)


xId = "91470304"
ccokie = "first_visit_datetime_pc=2022-08-06+03:53:37; p_ab_id=1; p_ab_id_2=5; p_ab_d_id=1897822829; yuid_b=IFV4MVY; privacy_policy_agreement=5; c_type=23; privacy_policy_notification=0; a_type=0; b_type=1; __utmc=235335808; __utmz=235335808.1675712222.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _gcl_au=1.1.1586580017.1675934633; _gid=GA1.2.67267752.1677021212; PHPSESSID=91470304_hbEoBFwL6Ss8hQHDiSkc26NAN2BgUaww; device_token=cbf72f380348bc4dcc9910df20a3b368; QSI_S_ZN_5hF4My7Ad6VNNAi=v:100:0; __utmv=235335808.|2=login ever=yes=1^3=plan=premium=1^5=gender=male=1^6=user_id=91470304=1^9=p_ab_id=1=1^10=p_ab_id_2=5=1^11=lang=en=1; _ga_MZ1NL4PHH0=GS1.1.1677021212.1.1.1677021635.0.0.0; __utma=235335808.1013236179.1675712222.1677021201.1677023923.4; login_ever=yes; __cf_bm=uIwLHChsA9lvfHUYdc_qU3KBp.pYrFxzrlv_4crFoE4-1677024971-0-AaFldWtGUM9OmDn1Kfcwc03QpGNuGGlE8Ev1PZtv6Q6PavyffvJ2dmVVIDVdeTM6cD8GNSLlL8ta93GxurhWiQqj+rxXEWgO3LDUqV0uXNORvDhI4+KP930Hf962s6ivFp1Zz6aG5fVGtpySkJBAEcVUAoxfpO6+KGijUP4sJAvftKvKK8NZaD6zcqDr47mOMJsHCvdck/DW4GqbSDeuIJo=; __utmt=1; tag_view_ranking=_EOd7bsGyl~ziiAzr_h04~azESOjmQSV~Ie2c51_4Sp~Lt-oEicbBr~WMwjH6DkQT~HY55MqmzzQ~yREQ8PVGHN~MnGbHeuS94~BSlt10mdnm~tgP8r-gOe_~fg8EOt4owo~b_rY80S-DW~1kqPgx5bT5~5oPIfUbtd6~KN7uxuR89w~QaiOjmwQnI~0Sds1vVNKR~pA1j4WTFmq~aPdvNeJ_XM~vzTU7cI86f~HHxwTpn5dx~pnCQRVigpy~eVxus64GZU~rOnsP2Q5UN~-98s6o2-Rp~EZQqoW9r8g~iAHff6Sx6z~jk9IzfjZ6n~PsltMJiybA~TqiZfKmSCg~IfWbVPYrW4~0TgyeJ7TQv~g2IyszmEaU~28gdfFXlY7~DCzSewSYcl~n15dndrA2h~CActc_bORM~U51WZv5L6G~-7RnTas_L3~zyKU3Q5L4C~QwUeUr8yRJ~j3leh4reoN~vgqit5QC27~t1Am7AQCDs~5cTBH7OrXg~-HnQonkV01~oCqKGRNl20~ba025Wj3s2~TAc-DD8LV2~p0NI-IYoo2~wqBB0CzEFh~U-RInt8VSZ~oiDfuNWtp4~fAWkkRackx~i54EuUSPdz~Js5EBY4gOW~ZQJ8wXoTHu~Cm1Eidma50~CMvJQbTsDH~ocDr8uHfOS~pzZvureUki~ZNRc-RnkNl~nWC-P2-9TI~q1r4Vd8vYK~hZzvvipTPD~DpYZ-BAzxm~096PrTDcN1~3WI2JuKHdp~faHcYIP1U0~1n-RsNEFpK~Bd2L9ZBE8q~txZ9z5ByU7~r01unnQL0a~EEUtbD_K_n~cb-9gnu4GK~npWJIbJroU~XbjPDXsKD-~lkoWqucyTw~P8OX_Lzc1b~RmnFFg7HS4~6rYZ-6JKHq~d80xTahBd1~OYl5wlor4w~2R7RYffVfj~1CWwi2xr7g~c7QmKEJ54V~rlExNugdTH~wO2lnVhO8m~vc2ipXnqbX~Is5E1jIZcw~c_aC4uL3np~vzxes78G4k; _ga=GA1.2.714813637.1675712223; _gat_UA-1830249-3=1; _ga_75BBYNYN9J=GS1.1.1677023923.4.1.1677025390.0.0.0; __utmb=235335808.52.9.1677024704913"

headers = {
    "accept-type": "application/json",
    "accept-encoding": "ru,en-US;q=0.9,en;q=0.8,uk;q=0.7,af;q=0.6",
    "language": "gzip, deflate, br",
    "cookie": ccokie,
    "dnt": "1",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    "x-user-id": xId,
    "referer": "https://www.pixiv.net/",
}

caches = TTLCache(maxsize=1000, ttl=300)  

async def get_dowload_img(link,size = None, thumbnail_size = None, cache = True):
    if cache:
        cache_key = json.dumps((link, size, thumbnail_size), sort_keys=True)  # Преобразовываем в строку
            
        if cache_key in caches:
            return caches[cache_key]
    

    try:
        if "pximg" in link:
            async with aiohttp.ClientSession(headers=headers) as session, session.get(link) as r:
                image = await r.read()
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(link) as response:
                    image = await response.read()
    except:
        raise
    
    image = Image.open(BytesIO(image)).convert("RGBA")
    if not size is None:
        image = image.resize(size)
        if cache:
            caches[cache_key] = image
        return image
    elif thumbnail_size is not None:
        image.thumbnail(thumbnail_size)
        if cache:
            caches[cache_key] = image
        return image
    else:
        if cache:
            caches[cache_key] = image
        return image


async def get_user_image(img, cache = True):
    if type(img) != str:
        img = img
    elif type(img) == str:
        linkImg = re.search("(?P<url>https?://[^\s]+)", img)
        if linkImg:
            try:
                img = await get_dowload_img(linkImg.group(),cache = cache)
            except Exception as e:
                raise
        else:
            img = Image.open(img)
    else:
        return None
    return img.convert("RGBA")

async def recolor_image(image, target_color):
    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    image = image.copy()

    pixels = image.load()
    for i in range(image.width):
        for j in range(image.height):
            r, g, b, a = pixels[i, j]
            if a != 0:  # Проверяем, является ли текущий пиксель непрозрачным
                pixels[i, j] = target_color + (a,)  # Заменяем цвет, включая прозрачность
    return image

async def light_level(img):
    stat = ImageStat.Stat(img)
    return stat.mean[0]

async def apply_opacity(image, opacity=0.2):
    """
    Изменяет непрозрачность изображения на указанный уровень, сохраняя прозрачность фона.
    
    :param image: Изображение (Image.Image).
    :param opacity: Уровень непрозрачности (0.0 - полностью прозрачное, 1.0 - непрозрачное).
    :return: Изображение с измененной непрозрачностью (Image.Image).
    """
    result_image = image.copy()
    alpha = result_image.split()[3]
    alpha = alpha.point(lambda p: int(p * opacity))
    result_image.putalpha(alpha)

    return result_image


async def resize_image(image, scale):
    width, height = image.size
    new_width = int(width * scale)
    new_height = int(height * scale)
    resized_image = image.resize((new_width, new_height))
    return resized_image


async def apply_soft_light(base_image,overlay_image, opacity=0.5):
    base_width, base_height = base_image.size
    overlay_image = overlay_image.resize((base_width, base_height))
    result = ImageChops.soft_light(base_image, overlay_image.convert("RGBA"))
    
    return result


async def get_centr_honkai_art(size, file_name):
    background_image = Image.new('RGBA', size, color=(0, 0, 0, 0))
    foreground_image = file_name.convert("RGBA")

    scale = max(size[0] / foreground_image.size[0], size[1] / foreground_image.size[1])
    foreground_image = foreground_image.resize((int(foreground_image.size[0] * scale), int(foreground_image.size[1] * scale)), resample=Image.LANCZOS)

    background_size = background_image.size
    foreground_size = foreground_image.size

    x = background_size[0] // 2 - foreground_size[0] // 2

    if foreground_size[1] > background_size[1]:
        y_offset = max(int(0.3 * (foreground_size[1] - background_size[1])), int(0.5 * (-foreground_size[1])))
        y = -y_offset
    else:
        y = background_size[1] // 2 - foreground_size[1] // 2

    background_image.alpha_composite(foreground_image, (x, y))

    return background_image

async def get_centr_honkai(size, file_name):
    background_image = Image.new('RGBA', size, color=(0, 0, 0, 0))
    foreground_image = file_name.convert("RGBA")

    scale = 0.65
    foreground_image = await resize_image(foreground_image, scale)

    background_size = background_image.size
    foreground_size = foreground_image.size

    x = background_size[0] // 2 - foreground_size[0] // 2
    y = background_size[1] // 2 - foreground_size[1] // 2

    background_image.alpha_composite(foreground_image, (x, y))

    return background_image

async def get_text_size_frame(text,font_size,frame_width):
    font = await get_font(font_size)

    while font.getlength(text) > frame_width:
        font_size -= 1
        font = await get_font(font_size)

    return font,font.getlength(text)



async def get_line_text(text, font, max_width):
    lines = []
    line = []
    for word in text.split():
        if line:
            temp_line = line + [word]
            temp_text = ' '.join(temp_line)
            temp_width = font.getmask(temp_text).getbbox()[2]
            if temp_width <= max_width:
                line = temp_line
            else:
                lines.append(line)
                line = [word]
        else:
            line = [word]
    if line:
        lines.append(line)
    
    return lines
        

async def get_width_height(lines,font):
    width = 0
    height = 0
    
    for line in lines:
        line_width = font.getmask(' '.join(line)).getbbox()[2]
        width = max(width, line_width)
        height += font.getmask(' '.join(line)).getbbox()[3]
    
    return width, height

async def get_new_font(max_height,height,font_size):
    if max_height is not None and height > max_height:
        reduction_ratio = max_height  / height
        new_font_size = int(font_size * reduction_ratio)
        font = await get_font(new_font_size)    
    else:
        font = await get_font(font_size)
    
    return font
    
        
async def create_image_text(text, font_size, max_width=336, max_height=None, color=(255, 255, 255, 255)):
        
    font = await get_font(font_size)
   
    lines = await get_line_text(text,font,max_width)

    width,height = await get_width_height(lines,font)
    
    font = await get_new_font(max_height,height,font_size)
    
    width,height = await get_width_height(lines,font)
    
    img = Image.new('RGBA', (min(width, max_width), height + (font_size - 4)), color=(255, 255, 255, 0))

    draw = ImageDraw.Draw(img)
    y_text = 0
    for line in lines:
        text_width, text_height = font.getmask(' '.join(line)).getbbox()[2:]
        draw.text((0, y_text), ' '.join(line), font=font, fill=color)
        y_text += text_height + 5

    return img

async def create_image_with_text(text, font_size, max_width=336, color=(255, 255, 255, 255), alg="Left"):
    font = await get_font(font_size)

    lines = []
    line = []
    for word in text.split():
        if line:
            temp_line = line + [word]
            temp_text = ' '.join(temp_line)
            temp_width = font.getmask(temp_text).getbbox()[2]
            if temp_width <= max_width:
                line = temp_line
            else:
                lines.append(line)
                line = [word]
        else:
            line = [word]
    if line:
        lines.append(line)

    width = 0
    height = 0
    for line in lines:
        line_width = font.getmask(' '.join(line)).getbbox()[2]
        width = max(width, line_width)
        height += font.getmask(' '.join(line)).getbbox()[3]

    img = Image.new('RGBA', (min(width, max_width), height + (font_size)), color=(255, 255, 255, 0))

    draw = ImageDraw.Draw(img)
    
    y_text = 0
    for line_num, line in enumerate(lines):
        text_width, text_height = font.getmask(' '.join(line)).getbbox()[2:]
        if alg == "center" and line_num > 0:
            x_text = (max_width - text_width) // 2
        else:
            x_text = 0
        draw.text((x_text, y_text), ' '.join(line), font=font, fill=color)
        y_text += text_height + 5

    return img



class GradientGenerator:
    def __init__(self, source_img_path):
        self.source_img = source_img_path
        self.frame = ()
        self.source_width, self.source_height = self.source_img.size

    async def generate(self, width, height, left = False):
        gradient_img = Image.new("RGB", (width, height))

        # Вычисляем ширину и высоту каждой полосы градиента
        top_height = height // 3
        bottom_height = height // 3
        center_height = height - top_height - bottom_height
        # Определяем координаты точек, с которых будем брать цвета
        if left:
            left = 3
            right = 4
        else:
            left = self.source_width - 142
            right = self.source_width - 141
        top_1 = 1
        bottom_1 = top_height - 1
        top_2 = top_height + 1
        bottom_2 = top_height + center_height - 1
        top_3 = top_height + center_height + 1
        bottom_3 = height - 2

        # Получаем цвета для каждой полосы
        top_color = await self._get_pixel_color(left, top_1, right, bottom_1)
        if top_color[0] > 209 and top_color[1] > 209 and top_color[2] >  209:
           top_color = (209,209,209)

        center_color = await self._get_pixel_color(left, top_2, right, bottom_2)
        if center_color[0] > 209 and center_color[1] > 209 and center_color[2] > 209:
           center_color = (209,209,209)

        bottom_color = await self._get_pixel_color(left, top_3, right, bottom_3)
        if bottom_color[0] > 209 and bottom_color[1] > 209 and bottom_color[2] >  209:
           bottom_color = (209,209,209)


        # Заполняем каждую полосу соответствующим цветом
        for y in range(top_height):
            for x in range(width):
                ratio = y / (top_height - 1)
                gradient_color = self._get_interpolated_color(top_color, center_color, ratio)
                gradient_img.putpixel((x, y), gradient_color)

        for y in range(center_height):
            for x in range(width):
                ratio = y / (center_height - 1)
                gradient_color = self._get_interpolated_color(center_color, bottom_color, ratio)
                gradient_img.putpixel((x, y + top_height), gradient_color)

        for y in range(bottom_height):
            for x in range(width):
                gradient_color = bottom_color
                gradient_img.putpixel((x, y + top_height + center_height), gradient_color)

        gradient_img
        return gradient_img

    async def _get_light_pixel_color(self,pixel_color):
        """
        Увеличивает яркость цвета на заданный коэффициент.
        
        :param color: Исходный цвет в формате (R, G, B), где R, G и B - значения от 0 до 255.
        :param factor: Коэффициент увеличения яркости (1.0 - оставить без изменений, больше 1.0 - увеличить).
        :return: Новый цвет с увеличенной яркостью.
        """               
        factor = 1.5
        r, g, b = pixel_color
        r = min(int(r * factor), 255)
        g = min(int(g * factor), 255)
        b = min(int(b * factor), 255)
        
        return (r, g, b)        
        
        #return pixel_color
            
    async def _get_pixel_color(self, left, top, right, bottom):
        cropped_img = self.source_img.crop((left, top, right, bottom))
        resized_img = cropped_img.convert("RGB").resize((1, 1))
        pixel_color = resized_img.getpixel((0, 0))

        text_pixel = Image.new("RGB", (1, 1),color=pixel_color)
        ll = await light_level(text_pixel)
        if ll < 45:
            pixel_color = await self._get_light_pixel_color(pixel_color)
        return pixel_color

    def _get_interpolated_color(self, start_color, end_color, ratio):
        return tuple(int(start_color[i] + (end_color[i] - start_color[i]) * ratio) for i in range(3))