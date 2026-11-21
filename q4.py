from PIL import Image, ImageDraw, ImageFont, ImageOps
import os, shutil, math

TIMP = 15      # secunde de gândire
REVEAL = 3     # secunde cu răspunsul
FPS = 20
intrebare = "Cât timp durează ca lumina solară\nsă ajungă pe Pământ?"
opts = ["2 minute", "4 minute", "8 minute"]
corect = 2     # 0 = A, 1 = B, 2 = C
culori = [(235, 60, 80), (50, 120, 240), (150, 80, 220)]

def font(size):
    for f in ["/system/fonts/Roboto-Bold.ttf", "/system/fonts/Roboto-Regular.ttf"]:
        if os.path.exists(f):
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()

F_mare, F_mic = font(50), font(44)

cale = os.path.expanduser("~/storage/downloads/poza.jpg")
baza = None
if os.path.exists(cale):
    baza = ImageOps.fit(Image.open(cale).convert("RGB"), (760, 535))

def usor(x):
    x = max(0, min(1, x))
    return 1 - (1 - x) ** 3

def poza(t):
    z = 1 + 0.15 * min(t / (TIMP + REVEAL), 1)
    w, h = 760 / z, 535 / z
    x0, y0 = (760 - w) / 2, (535 - h) / 2
    return baza.crop((int(x0), int(y0), int(x0 + w), int(y0 + h))).resize((540, 380))

def cadru(k):
    t = k / FPS
    raspuns = t >= TIMP
    ramase = max(0, math.ceil(TIMP - t))
    progres = min(t / TIMP, 1)
    tr = t - TIMP

    img = Image.new("RGB", (1280, 720), (255, 150, 20))
    d = ImageDraw.Draw(img)
    d.text((60, 35), intrebare, font=F_mare, fill="white")

    # poza: intră din stânga, apoi face zoom lent
    px = 50 - int((1 - usor(t / 0.7)) * 700)
    d.rounded_rectangle((px, 230, px + 580, 640), radius=30, fill="white")
    if baza:
        img.paste(poza(t), (px + 20, 250))
    else:
        d.text((px + 150, 420), "lipsește poza.jpg", font=F_mic, fill="gray")

    # răspunsuri: intră pe rând din dreapta
    for i, o in enumerate(opts):
        y = 230 + i * 130
        start = 0.4 + i * 0.4
        x = 680 + int((1 - usor((t - start) / 0.6)) * 700)
        g = 0
        if raspuns:
            if i == corect:
                fundal = (60, 220, 90)
                g = int(6 + 6 * math.sin(tr * 8))   # pulsează
            else:
                fundal = (200, 200, 200)
        else:
            fundal = "white"
        d.rounded_rectangle((x - g, y - g, x + 560 + g, y + 105 + g), radius=52, fill=fundal)
        d.ellipse((x + 10, y + 8, x + 100, y + 98), fill=culori[i])
        d.text((x + 32, y + 22), "ABC"[i], font=F_mic, fill="white")
        d.text((x + 130, y + 26), o, font=F_mic, fill="black")

    # bara de timp
    d.rounded_rectangle((60, 665, 1100, 705), radius=20, fill=(240, 240, 240))
    rosu = ramase <= 3 and not raspuns
    if progres > 0.03:
        d.rounded_rectangle((60, 665, 60 + int(1040 * progres), 705), radius=20,
                            fill=(230, 40, 40) if rosu else (40, 200, 90))
    if raspuns:
        d.text((1120, 658), "Corect!", font=F_mic, fill="white")
    else:
        d.text((1160, 650), str(ramase), font=F_mare, fill="white")
    return img

if os.path.exists("frames"):
    shutil.rmtree("frames")
os.makedirs("frames")

for k in range(int((TIMP + REVEAL) * FPS)):
    cadru(k).save(f"frames/f{k:04d}.png")
