from PIL import Image, ImageOps

import disnake


async def invert_pfp(user):
    await user.avatar.with_static_format('jpg').save(fp='inverted_avatar.png')
    img = Image.open('inverted_avatar.png')
    im_invert = ImageOps.invert(img)
    im_invert.save('inverted_avatar.png')
    file = disnake.File(fp='inverted_avatar.png', filename=f'{user.display_name}_inverted_avatar.png')
    return file
