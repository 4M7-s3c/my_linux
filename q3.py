from PIL import Image, ImageDraw, ImageFont, ImageOps
import os, shutil

TIMP = 15   # secunde de gândire
FPS = 10
intrebare = "Cât timp durează ca lumina solară\nsă ajungă pe Pământ?"
opts = ["2 minute", "4 minute", "8 minute"]
corect = 2   # 0 = A, 1 = B, 2 = C
culori = [(235, 60, 80), (50, 120, 240), (150, 80, 220)]

def font(size):
    for f in ["/system/fonts/Roboto-Bold.ttf", "/system/fonts/Roboto-Regular.ttf"]:
        if os.path.exists(f):
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()

F_mare, F_mic = font(50), font(44)
cale = os.path.expanduser("~/storage/downloads/poza.jpg")
foto = None
if os.path.exists(cale):
    foto = ImageOps.fit(Image.open(cale).convert("RGB"), (540, 380))

if os.path.exists("frames"):
    shutil.rmtree("frames")
os.makedirs("frames")

def cadru(progres, ramase, raspuns):
    img = Image.new("RGB", (1280, 720), (255, 150, 20))
    d = ImageDraw.Draw(img)
    d.text((60, 35), intrebare, font=F_mare, fill="white")
    # poza
    d.rounded_rectangle((50, 230, 630, 640), radius=30, fill="white")
    if foto:
        img.paste(foto, (70, 250))
    else:
        d.text((200, 420), "lipsește poza.jpg", font=F_mic, fill="gray")
    # variante
    for i, o in enumerate(opts):
        y = 230 + i * 130
        if raspuns:
            fundal = (60, 220, 90) if i == corect else (200, 200, 200)
        else:
            fundal = "white"
        d.rounded_rectangle((680, y, 1240, y + 105), radius=52, fill=fundal)
        d.ellipse((690, y + 8, 780, y + 98), fill=culori[i])
        d.text((712, y + 22), "ABC"[i], font=F_mic, fill="white")
        d.text((810, y + 26), o, font=F_mic, fill="black")
    # bara + numărătoare
    d.rounded_rectangle((60, 665, 1100, 705), radius=20, fill=(240, 240, 240))
    culoare_bara = (230, 40, 40) if ramase <= 3 and not raspuns else (40, 200, 90)
    if progres > 0.03:
        d.rounded_rectangle((60, 665, 60 + int(1040 * progres), 705), radius=20, fill=culoare_bara)
    if raspuns:
        d.text((1130, 655), "Corect!", font=F_mic, fill="white")
    else:
        d.text((1160, 655), str(ramase), font=F_mare, fill="white")
    return img

total = TIMP * FPS
n = 0
for k in range(total):
    cadru(k / (total - 1), TIMP - k // FPS, False).save(f"frames/f{n:04d}.png")
    n += 1
for k in range(3 * FPS):
    cadru(1, 0, True).save(f"frames/f{n:04d}.png")
    n += 1
