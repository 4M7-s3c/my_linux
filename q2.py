from PIL import Image, ImageDraw, ImageFont
import os

font = ImageFont.truetype("/system/fonts/Roboto-Regular.ttf", 44)
intrebare = "Cât timp durează ca lumina solară\nsă ajungă pe Pământ?"
opts = ["A   2 minute", "B   4 minute", "C   8 minute"]
corect = 2
os.makedirs("frames", exist_ok=True)

def cadru(progres, raspuns):
    img = Image.new("RGB", (1280, 720), (255, 140, 0))
    d = ImageDraw.Draw(img)
    d.text((60, 40), intrebare, font=font, fill="white")
    for i, o in enumerate(opts):
        y = 250 + i * 130
        culoare = (60, 220, 90) if (raspuns and i == corect) else "white"
        d.rounded_rectangle((700, y, 1220, y + 100), radius=50, fill=culoare)
        d.text((740, y + 25), o, font=font, fill="black")
    d.rounded_rectangle((200, 640, 1080, 680), radius=20, fill=(235, 235, 235))
    if progres > 0.05:
        d.rounded_rectangle((200, 640, 200 + int(880 * progres), 680), radius=20, fill=(40, 200, 90))
    return img

n = 0
for k in range(50):
    cadru(k / 49, False).save(f"frames/f{n:03d}.png")
    n += 1
for k in range(20):
    cadru(1, True).save(f"frames/f{n:03d}.png")
    n += 1
