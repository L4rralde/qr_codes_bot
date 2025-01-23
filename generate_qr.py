import segno
from db import DB, Amigo

def generate_qr(name: str, path: str) -> None:
    qrcode = segno.make_qr(name)
    qrcode.save(path)

def generate_amigo_qr(amigo: Amigo) -> None:
    

if __name__ == '__main__':
    for amigo in DB:
        

