from PIL import Image, ImageDraw, ImageFont

img = Image.new("RGB", (1280, 720), (255, 140, 0))
d = ImageDraw.Draw(img)
font = ImageFont.truetype("/system/fonts/Roboto-Regular.ttf", 44)

d.text((60, 40), "Cât timp durează ca lumina solară\nsă ajungă pe Pământ?", font=font, fill="white")

opts = ["A   2 minute", "B   4 minute", "C   8 minute"]
for i, o in enumerate(opts):
    y = 250 + i * 130
    d.rounded_rectangle((700, y, 1220, y + 100), radius=50, fill="white")
    d.text((740, y + 25), o, font=font, fill="black")

img.save("q1.png")
