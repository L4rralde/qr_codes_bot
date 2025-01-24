"""
Functions and script to generate qr codes given an Amigo instance
"""

import os

from PIL import Image
from PIL import ImageDraw
import segno

from db import AMIGOS, Amigo
from misc import GIT_ROOT


def generate_amigo_qr(amigo: Amigo) -> None:
    """
    Generates the qr of a given amigo
    """
    path = f"{GIT_ROOT}/images/{amigo.curp}.png"
    qrcode = segno.make_qr(f"SCE/{amigo.curp}")
    qrcode.save(path)
    im = Image.open(path)
    im = im.resize((4*im.size[0], 4*im.size[1]), Image.Resampling.LANCZOS)
    new_im = Image.new(
        'RGB',
        (2*im.size[0], 2*im.size[1]),
        color = "white"
    )
    new_im.paste(im, (im.size[0]//2, im.size[1]//2))
    draw = ImageDraw.Draw(new_im)
    draw.text((10, 10), amigo.name, (0, 0, 0))
    new_im.save(path)

def generate_agg_qr(amigos_qr: list, path: str) -> None:
    """
    Generates an image comprised by the qrs of a list of Amigos
    """
    images = [
        Image.open(amigo_qr.qr_path)
        for amigo_qr in amigos_qr
    ]
    widths, heights = zip(*(i.size for i in images))
    max_width = max(widths)
    max_height = max(heights)
    new_im = Image.new(
        'RGB',
        (max_width*2, max_height*((len(images) - 1)//2 + 1)),
        color = "white"
    )
    x_offset = 0
    y_offset = 0
    for i, im in enumerate(images):
        x_offset = im.size[0] * (i%2)
        y_offset = im.size[1] * (i//2)
        new_im.paste(im, (x_offset, y_offset))

    new_im.save(path)


class AmigoQR(Amigo):
    """
    Class of a Passenger friend with it's respective QR code
    """
    def __init__(self, amigo: Amigo) -> None:
        super().__init__(amigo.name, amigo.curp)
        self.qr_path = f"{GIT_ROOT}/images/{amigo.curp}.png"
        if not os.path.exists(self.qr_path):
            generate_amigo_qr(amigo)


def main():
    """
    Script: Generates qr codes for each Amigo in DB
    """
    for amigo in AMIGOS:
        generate_amigo_qr(amigo)

if __name__ == '__main__':
    main()
