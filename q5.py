import os, math, glob, random, subprocess, colorsys
from PIL import Image, ImageDraw, ImageFont, ImageOps

# ===== SETĂRI: aici schimbi tu =====
intrebare = "Cât timp durează ca lumina solară\nsă ajungă pe Pământ?"
opts = ["2 minute", "4 minute", "8 minute"]
corect = 2             # 0 = A, 1 = B, 2 = C
TIMP = 15              # secunde de gândire
FPS = 15               # 20 = mai fluid, dar durează mai mult
POZA = os.path.expanduser("~/storage/downloads/poza.jpg")
IESIRE = os.path.expanduser("~/storage/downloads/q5.mp4")
FUN_RASPUNSURI = True  # font jucăuș la răspunsuri
W, H = 1280, 720
CULORI = [(255, 70, 95), (40, 140, 255), (165, 90, 240)]

# ===== FONTURI =====
def gaseste(tipare):
    for t in tipare:
        g = sorted(glob.glob("/system/fonts/" + t))
        if g:
            return g[0]
    return None

CALE_TITLU = gaseste(["Roboto-Black.ttf", "Roboto-Bold.ttf", "*Bold*.ttf",
                      "Roboto-Regular.ttf", "*.ttf"])
CALE_FUN = gaseste(["ComingSoon.ttf", "DancingScript-Bold.ttf"]) if FUN_RASPUNSURI else None
if CALE_FUN is None:
    CALE_FUN = CALE_TITLU
print("Font titlu:", CALE_TITLU)
print("Font răspunsuri:", CALE_FUN)

F_titlu = ImageFont.truetype(CALE_TITLU, 58)
F_lit = ImageFont.truetype(CALE_TITLU, 54)
F_mic = ImageFont.truetype(CALE_TITLU, 44)
F_rasp = ImageFont.truetype(CALE_FUN, 52)

# ===== VOCEA (gTTS, are nevoie de internet) =====
litere = "ABC"
texte_voce = [intrebare.replace("\n", " ")]
texte_voce += [f"{litere[i]}. {opts[i]}" for i in range(3)]
texte_voce += [f"Răspunsul corect este {litere[corect]}: {opts[corect]}!"]

def durata(fisier):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", fisier], capture_output=True, text=True)
    return float(r.stdout.strip())

os.makedirs("voce", exist_ok=True)
try:
    from gtts import gTTS
    for i, txt in enumerate(texte_voce):
        gTTS(txt, lang="ro").save(f"voce/v{i}.mp3")
except Exception as e:
    print("Nu am putut face vocea (ai internet?):", e)
    raise SystemExit
d = [durata(f"voce/v{i}.mp3") for i in range(5)]

# ===== CRONOLOGIA (în secunde) =====
T_Q = 0.3
s = []
cur = T_Q + d[0] + 0.5
for i in range(3):
    s.append(cur)
    cur += d[i + 1] + 0.4
T0 = cur + 0.5          # începe gândirea
T1 = T0 + TIMP          # apare răspunsul
T_R = T1 + 0.4          # vocea spune răspunsul
TOTAL = max(T1 + 4.0, T_R + d[4] + 1.5)
NF = int(TOTAL * FPS)
print(f"Videoclip de {TOTAL:.0f} secunde, {NF} cadre")

# ===== SUNETUL =====
expr = (f"0.05*(sin(2*PI*262*t)+sin(2*PI*330*t)+sin(2*PI*392*t))*(0.75+0.25*sin(2*PI*0.4*t))"
        f"+0.30*sin(2*PI*880*t)*between(t,{T0:.2f},{T1:.2f})*lt(mod(t-{T0:.2f},1),0.05)"
        f"+0.45*sin(2*PI*1320*t)*gte(t,{T1:.2f})*exp(-3*(t-{T1:.2f}))"
        f"+0.30*sin(2*PI*1760*t)*gte(t,{T1 + 0.15:.2f})*exp(-4*(t-{T1 + 0.15:.2f}))")
delays = [T_Q] + s + [T_R]
cmd = ["ffmpeg", "-y", "-loglevel", "error"]
for i in range(5):
    cmd += ["-i", f"voce/v{i}.mp3"]
cmd += ["-f", "lavfi", "-i", f"aevalsrc='{expr}':s=44100:d={TOTAL:.2f}"]
filtre = ";".join(
    f"[{i}:a]adelay={int(delays[i] * 1000)}:all=1,volume=1.2,aresample=44100[a{i}]"
    for i in range(5))
filtre += ";[a0][a1][a2][a3][a4][5:a]amix=inputs=6:duration=longest:normalize=0,alimiter=limit=0.95[out]"
cmd += ["-filter_complex", filtre, "-map", "[out]", "-ac", "2", "-t", f"{TOTAL:.2f}", "audio.wav"]
print("Fac sunetul...")
if subprocess.run(cmd).returncode != 0:
    print("Eroare la sunet. Copiază mesajul de mai sus și trimite-mi-l.")
    raise SystemExit

# ===== FUNDALUL VIU =====
GRAD = Image.linear_gradient("L").resize((W, H))
random.seed(7)
BULE = [dict(x=random.randint(0, W), r=random.randint(25, 90), v=random.randint(25, 70),
             y0=random.randint(0, H), h=random.random(), f=random.random() * 6)
        for _ in range(22)]
CONF = [(random.randint(0, W), random.uniform(0, 1.2), random.uniform(180, 420),
         random.random(), random.randint(10, 20)) for _ in range(70)]

def culoare(h, sat=0.75, val=1.0):
    r, g, b = colorsys.hsv_to_rgb(h % 1, sat, val)
    return (int(r * 255), int(g * 255), int(b * 255))

def fundal(t):
    h = t * 0.04
    img = ImageOps.colorize(GRAD, culoare(h), culoare(h + 0.66), mid=culoare(h + 0.33))
    dr = ImageDraw.Draw(img, "RGBA")
    for b in BULE:
        y = (b["y0"] - b["v"] * t) % (H + 2 * b["r"]) - b["r"]
        x = b["x"] + 30 * math.sin(t * 0.8 + b["f"])
        c = culoare(b["h"] + t * 0.05, 0.4, 1.0)
        dr.ellipse((x - b["r"], y - b["r"], x + b["r"], y + b["r"]), fill=c + (55,))
    return img

# ===== POZA =====
FW, FH = 960, 680
if os.path.exists(POZA):
    FOTO = ImageOps.fit(Image.open(POZA).convert("RGB"), (FW, FH))
else:
    FOTO = Image.new("RGB", (FW, FH), (120, 120, 200))
    ImageDraw.Draw(FOTO).text((300, 320), "lipseste poza.jpg", fill="white")
MASCA = Image.new("L", (480, 340), 0)
ImageDraw.Draw(MASCA).rounded_rectangle((0, 0, 479, 339), radius=24, fill=255)

def card_poza(t):
    z = 1 + 0.5 * min(t / TOTAL, 1)
    w, h = FW / z, FH / z
    cx = FW / 2 + (FW - w) / 2 * 0.7 * math.sin(t * 0.6)
    cy = FH / 2 + (FH - h) / 2 * 0.7 * math.cos(t * 0.45)
    box = (int(cx - w / 2), int(cy - h / 2), int(cx + w / 2), int(cy + h / 2))
    f = FOTO.crop(box).resize((480, 340), Image.BICUBIC)
    c = Image.new("RGBA", (560, 400), (0, 0, 0, 0))
    ImageDraw.Draw(c).rounded_rectangle((0, 0, 559, 399), radius=38, fill="white")
    c.paste(f, (40, 30), MASCA)
    return c.rotate(2.5 * math.sin(t * 1.3), resample=Image.BICUBIC, expand=True)

# ===== AJUTOARE =====
def usor(x):
    x = max(0, min(1, x))
    return 1 - (1 - x) ** 3

def revenire(x):   # intră cu o mică săritură
    x = max(0, min(1, x))
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2

def scrie1(dr, xy, text, f, fill="white", contur=(60, 20, 100), sw=6, anchor="lm"):
    x, y = xy
    dr.text((x + 4, y + 6), text, font=f, fill=(25, 0, 50), stroke_width=sw,
            stroke_fill=(25, 0, 50), anchor=anchor)
    dr.text((x, y), text, font=f, fill=fill, stroke_width=sw, stroke_fill=contur, anchor=anchor)

def scriem(dr, xy, text, f, fill="white", contur=(60, 20, 100), sw=7):
    x, y = xy
    dr.multiline_text((x + 5, y + 7), text, font=f, fill=(25, 0, 50), stroke_width=sw,
                      stroke_fill=(25, 0, 50), spacing=10)
    dr.multiline_text((x, y), text, font=f, fill=fill, stroke_width=sw,
                      stroke_fill=contur, spacing=10)

# ===== UN CADRU =====
CW, CH = 580, 110

def cadru(t):
    img = fundal(t)
    dr = ImageDraw.Draw(img, "RGBA")
    reveal = t >= T1
    tr = t - T1

    # întrebarea, scrisă literă cu literă
    dr.rounded_rectangle((30, 20, W - 30, 200), radius=45, fill=(25, 0, 70, 120),
                         outline=(255, 255, 255, 200), width=4)
    nr = int(max(0, min(1, (t - T_Q) / d[0])) * len(intrebare))
    vis = intrebare[:nr]
    if nr < len(intrebare) and int(t * 4) % 2 == 0:
        vis += "|"
    scriem(dr, (70, 38), vis, F_titlu)

    # poza
    c = card_poza(t)
    cxm = 330 - int((1 - usor((t - 0.3) / 0.8)) * 700)
    cym = 425 + int(8 * math.sin(t * 2))
    pos = (cxm - c.width // 2, cym - c.height // 2)
    img.paste((0, 0, 0), (pos[0] + 10, pos[1] + 14), c.split()[3].point(lambda a: a * 80 // 255))
    img.paste(c, pos, c)

    # răspunsurile
    for i, o in enumerate(opts):
        if t < s[i]:
            continue
        y = 235 + i * 130
        p = revenire((t - s[i]) / 0.6)
        x = 660 + int((1 - p) * 700)
        if not reveal:
            y += int(6 * math.sin(t * 2.5 + i * 1.7))
        col = CULORI[i]
        fc, oc, tc, g = col, (255, 255, 255), "white", 0
        if reveal:
            if i == corect:
                fc, oc, g = (50, 205, 90), (255, 235, 60), int(7 + 7 * math.sin(tr * 9))
            else:
                fc, tc = (185, 185, 200), (240, 240, 250)
                x += int(25 * usor(tr / 0.4))
        inchis = tuple(int(v * 0.45) for v in fc)
        dr.rounded_rectangle((x - g + 8, y - g + 10, x + CW + g + 8, y + CH + g + 10),
                             radius=55, fill=(0, 0, 0, 70))
        dr.rounded_rectangle((x - g, y - g, x + CW + g, y + CH + g), radius=55,
                             fill=fc, outline=oc, width=9)
        bx, by = x + 70, y + CH // 2
        dr.ellipse((bx - 44, by - 44, bx + 44, by + 44), fill="white")
        if reveal and i == corect:
            dr.line([(bx - 24, by), (bx - 6, by + 18), (bx + 26, by - 20)],
                    fill=(50, 205, 90), width=13, joint="curve")
        else:
            dr.text((bx, by), "ABC"[i], font=F_lit, fill=fc if reveal else col, anchor="mm")
        scrie1(dr, (x + 140, y + CH // 2), o, F_rasp, fill=tc, contur=inchis, sw=5)

    # bara de timp + numărătoarea
    tb = t - (T0 - 0.5)
    if tb > 0:
        yb = 650 + int((1 - usor(tb / 0.5)) * 90)
        dr.rounded_rectangle((60, yb, 1080, yb + 44), radius=22, fill=(255, 255, 255, 210))
        prog = max(0, min(1, (t - T0) / TIMP))
        ramase = max(0, math.ceil(T1 - t))
        rosu = ramase <= 3 and not reveal
        if prog > 0.03:
            dr.rounded_rectangle((60, yb, 60 + int(1020 * prog), yb + 44), radius=22,
                                 fill=(235, 45, 45) if rosu else (45, 205, 95))
        if reveal:
            scrie1(dr, (1100, yb + 22), "Corect!", F_mic)
        elif t >= T0:
            pop = max(0, 1 - ((t - T0) % 1) * 5)
            r = 40 + int(8 * pop)
            ccx, ccy = 1170, yb + 22
            dr.ellipse((ccx - r, ccy - r, ccx + r, ccy + r),
                       fill=(235, 45, 45) if rosu else "white")
            dr.text((ccx, ccy), str(ramase), font=F_lit, anchor="mm",
                    fill="white" if rosu else (60, 20, 100))

    # confetti
    if reveal:
        for (x0, dl, vel, hh, sz) in CONF:
            if tr > dl:
                yy = -30 + (tr - dl) * vel
                if yy < H:
                    xx = x0 + 35 * math.sin(tr * 4 + hh * 6)
                    dr.rectangle((xx, yy, xx + sz, yy + sz * 0.6), fill=culoare(hh, 0.9, 1.0) + (255,))
    return img

# ===== VIDEOCLIPUL =====
err = open("ffmpeg_err.txt", "w")
p = subprocess.Popen(
    ["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS),
     "-vcodec", "mjpeg", "-i", "pipe:0", "-i", "audio.wav",
     "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "20",
     "-c:a", "aac", "-b:a", "160k", "-shortest", IESIRE],
    stdin=subprocess.PIPE, stderr=err)
try:
    for k in range(NF):
        cadru(k / FPS).save(p.stdin, "JPEG", quality=92)
        if k % 15 == 0:
            print(f"\rcadru {k + 1}/{NF}", end="", flush=True)
    p.stdin.close()
    p.wait()
    print("\nGata! Videoclipul e aici:", IESIRE)
except BrokenPipeError:
    print("\nFFmpeg s-a oprit. Trimite-mi conținutul din ffmpeg_err.txt (cat ffmpeg_err.txt)")
