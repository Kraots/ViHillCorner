import numpy as np

from PIL import Image, ImageFont, ImageDraw

import disnake

from utils.helpers import run_in_executor

GRAY = (48, 48, 48)
ORANGE = (255, 128, 0)
TRANSPARENT = (0, 0, 0, 0)
BLUE = (22, 160, 245)
BLACK = (0, 0, 0)
TTF_FONT = 'games/assets/Milliard.otf'


@run_in_executor
def draw_progress_bar(d, x, y, w, h, progress, bg="white", fg="black"):
    # draw background
    d.ellipse((x + w, y, x + h + w, y + h), fill=bg)
    d.ellipse((x, y, x + h, y + h), fill=bg)
    d.rectangle((x + (h / 2), y, x + w + (h / 2), y + h), fill=bg)

    # draw progress bar
    w *= progress
    if w != 0.0:
        d.ellipse((x + w, y, x + h + w, y + h), fill=fg)
        d.ellipse((x, y, x + h, y + h), fill=fg)
        d.rectangle((x + (h / 2), y, x + w + (h / 2), y + h), fill=fg)

    return d


def get_font(text, image):
    fontsize = 1
    font = ImageFont.truetype(TTF_FONT, fontsize)
    while font.getsize(text)[0] < image.size[0]:
        fontsize += 1
        font = ImageFont.truetype(TTF_FONT, fontsize)
    while font.getsize(text)[1] > image.size[1]:
        fontsize -= 1
        font = ImageFont.truetype(TTF_FONT, fontsize)
    fontsize -= 1
    font = ImageFont.truetype(TTF_FONT, fontsize)
    return font


async def rank_card(user, level: int, rank: int, members_count: int, current_xp: int, needed_xp: int, percentage: float):
    max_lvl = False
    if level == 500:
        max_lvl = True

    img = Image.new("RGBA", (1000, 350), GRAY)

    if user.avatar is None:
        await user.display_avatar.save(fp='avatar.png')
    else:
        await user.avatar.with_static_format('jpg').save(fp='avatar.png')
    av = Image.open('avatar.png')
    av = av.resize((250, 250))
    h, w = av.size
    npImage = np.array(av)
    new_img = Image.new('L', av.size, 0)
    draw = ImageDraw.Draw(new_img)
    draw.pieslice([0, 0, h, w], 0, 360, fill=255)
    np_new = np.array(new_img)
    npImage = np.dstack((npImage, np_new))
    final_img = Image.fromarray(npImage)
    final_img.thumbnail((250, 250))
    final_img.save('avatar.png')
    av = Image.open('avatar.png').convert('RGBA')

    orange_line = Image.new("RGBA", (500, 10), ORANGE)

    _user = Image.new("RGBA", (500, 50), TRANSPARENT)
    draw = ImageDraw.Draw(_user)
    txt = str(user.display_name) + '#' + str(user.discriminator)
    font = get_font(txt, _user)
    draw.text((0, 0), txt, font=font)

    has_xp = Image.new("RGBA", (200, 40), TRANSPARENT)
    draw = ImageDraw.Draw(has_xp)
    font = ImageFont.truetype(TTF_FONT, 35)
    draw.text((0, 0), f"{current_xp:,}xp", font=font, fill=BLACK)

    percent = Image.new("RGBA", (140, 40), TRANSPARENT)
    draw = ImageDraw.Draw(percent)
    font = ImageFont.truetype(TTF_FONT, 35)
    if max_lvl is not True:
        draw.text((10, 0), f"{percentage}%", font=font, fill=BLACK)
    else:
        draw.text((10, 0), "MAX", font=font, fill=BLACK)

    next_xp = Image.new("RGBA", (200, 40), TRANSPARENT)
    draw = ImageDraw.Draw(next_xp)
    font = ImageFont.truetype(TTF_FONT, 35)
    if len(str(needed_xp)) == 3:
        z = f"    {needed_xp:,}xp"
    else:
        z = f"{needed_xp:,}xp"
    draw.text((0, 0), z, font=font, fill=BLACK)

    progressbar = Image.new("RGBA", (750, 50), (0, 0, 0, 0))
    d = ImageDraw.Draw(progressbar)
    d = await draw_progress_bar(d, 0, 0, 650, 45, percentage / 100, fg=BLUE)

    _rank = Image.new("RGBA", (235, 100))
    draw = ImageDraw.Draw(_rank)
    font = ImageFont.truetype(TTF_FONT, 35)
    draw.text((0, 0), f"     Rank:\n        {rank}/{members_count}", font=font)

    _level = Image.new("RGBA", (235, 100))
    draw = ImageDraw.Draw(_level)
    font = ImageFont.truetype(TTF_FONT, 35)
    if max_lvl is not True:
        draw.text((0, 0), f"     Level:\n        {level}", font=font)
    else:
        draw.text((0, 0), "     Level:\n       500(Max)", font=font)

    img.paste(im=av, mask=av, box=(10, 50))
    img.paste(im=orange_line, box=(350, 100))
    img.paste(im=_user, mask=_user, box=(350, 50))
    img.paste(im=progressbar, mask=progressbar, box=(275, 250))
    if max_lvl is not True:
        img.paste(im=has_xp, mask=has_xp, box=(285, 260))
        img.paste(im=next_xp, mask=next_xp, box=(800, 260))
    img.paste(im=percent, mask=percent, box=(550, 260))
    img.paste(im=_rank, mask=_rank, box=(325, 125))
    img.paste(im=_level, mask=_level, box=(600, 125))
    img.save('rank_card.png')

    f = disnake.File(fp='rank_card.png', filename='rank_card.png')

    return f
