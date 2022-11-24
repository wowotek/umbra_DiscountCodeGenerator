import qrcode
from PIL import Image, ImageDraw, ImageFont
import random, io, time


def random_card_number():
    data = []
    for _ in range(6):
        d = []
        for _ in range(5):
            d.append("0123456789"[random.randint(0, 9)])
        data.append("".join(d))

    return data

def delete_eye(matrix: list[list[int]]):
    coords = [
        ((2, 2), (9, 9)),
        ((32, 2), (39, 9)),
        ((2, 32), (9, 39))
    ]
    for coord in coords:
        for x in range(coord[0][0], coord[1][0], 1):
            for y in range(coord[0][1], coord[1][1], 1):
                matrix[x][y] = 0

    # for x in range(len(matrix)):
    #     for y in range(len(matrix[x])):
    #         matrix[x][y] = 1

    return matrix

def get_eye(size: int, data_color: tuple[int, int, int, int] = (0, 0, 0, 255), bg_color: tuple[int, int, int, int] = (255, 255, 255, 0)):
    s = (size, size)
    img = Image.new("RGBA", s)
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle((0, 0, size, size), radius=size/8, fill=data_color)
    draw.rounded_rectangle((size/8, size/8, size - (size/8), size - (size/8)), radius=size/8, fill=bg_color)
    draw.rounded_rectangle((size/4, size/4, size - (size/4), size - (size/4)), radius=size/8, fill=data_color)

    return img, Image.new("RGBA", s, "white")

def get_data_point(size: int, data: int, color):
    s = (size, size)
    if data == 0: return Image.new("RGBA", s, (0, 0, 0, 0)), Image.new("RGBA", s, "white")
    img = Image.new("RGBA", s)
    draw = ImageDraw.Draw(img)

    draw.ellipse((0, 0, size-1, size-1), color)
    # draw.ellipse((size/28, size/28, size - (size/28), size - (size/28)), (color[0], color[1], color[2], 120))
    # draw.ellipse((size/19, size/19, size - (size/19), size - (size/19)), (color[0], color[1], color[2], 190))
    # draw.ellipse((size/ 8, size/ 8, size - (size/ 8), size - (size/ 8)), (color[0], color[1], color[2], 220))
    # draw.ellipse((size/ 6, size/ 6, size - (size/ 6), size - (size/ 6)), (color[0], color[1], color[2], 255))

    return img, Image.new("RGBA", s, "white")


def generateQrCode(data: str, version: int):
    qr = qrcode.QRCode(
        version=5,
        error_correction=qrcode.ERROR_CORRECT_H,
        box_size=50,
        border=2
    )
    qr.add_data(data)
    mat = delete_eye([[1 if j else 0 for j in i] for i in qr.get_matrix()])
    qr = qr.make_image()

    img = Image.new("RGBA", qr.size, "#ffffff00")
    # img.paste(qr)
    idraw = ImageDraw.Draw(img)
    idraw.rounded_rectangle((0, 0, img.size[0]-1, img.size[0]-1), img.size[0]/15, "#ffffff")

    # Add Data Points
    m = 50
    y = 5
    for i in range(len(mat)):
        color = "#002366"
        # if((len(mat) / 2) - 2 <= i <= (len(mat) / 2) + 2):
        #     color = "#0046aa"
        x = 6
        for j in range(len(mat[i])):
            dp = get_data_point(img.size[0]//52, mat[i][j], color)
            if version == 1:
                img.paste(dp[0], (x, y), dp[0])
            elif version == 2:
                img.paste(dp[0], (x, y), dp[0])
                if ((0 <= i <=7 and 9 <= j <= 31) or (32 <= i <= 39 and 9 <= j <= 32)):
                    try:
                        if(mat[i+1][j] == 1):
                            for yy in range(2, 50, 2):
                                img.paste(dp[0], (x, y+yy), dp[0])
                    except: pass
                
                if ((0 <= j <=7 and 9 <= i <= 31) or (32 <= j <= 39 and 9 <= i <= 32)):
                    try:
                        if(mat[i][j+1] == 1):
                            for xx in range(2, 50, 2):
                                img.paste(dp[0], (x+xx, y), dp[0])
                    except: pass
                
                if (j <= i <= 39 - j and 9 <= j <= 13):
                    try:
                        if(mat[i+1][j] == 1):
                            for yy in range(2, 50, 2):
                                img.paste(dp[0], (x, y+yy), dp[0])
                    except: pass
                
                if (27 + -j + 13 <= i <= j - 1 and 27 <= j <= 31):
                    try:
                        if(mat[i+1][j] == 1):
                            for yy in range(2, 50, 2):
                                img.paste(dp[0], (x, y+yy), dp[0])
                    except: pass

                a = 0
                for xx in range(9, 18, 1):
                    if 9 <= i <= xx and (9 + a) <= j <= (30 - a):
                        try:
                            if(mat[i][j+1] == 1):
                                for xx in range(2, 50, 2):
                                    img.paste(dp[0], (x+xx, y), dp[0])
                        except: pass
                    a += 1
                    if a >= 5: a = 5
                
                a = 0
                for xx in range(9, 18, 1):
                    if 9 <= i + a - 22 <= xx + 0 and 9 + a <= j <= 30 - a:
                        try:
                            if(mat[i][j+1] == 1):
                                for xx in range(2, 50, 2):
                                    img.paste(dp[0], (x+xx, y), dp[0])
                        except: pass
                    a += 1
                
                for xx in range(9, 12, 1):
                    if 23 <= i <= xx + 15 and 14 <= j <= 25:
                        try:
                            if(mat[i][j+1] == 1):
                                for xx in range(2, 50, 2):
                                    img.paste(dp[0], (x+xx, y), dp[0])
                        except: pass
            x = x + int(img.size[0]/41)
        y = y + int(img.size[0]/41)

    # Add Eyes
    eye = get_eye(int(img.size[0]/5.8), "#002366")
    img.paste(eye[0], (img.size[0]//21, img.size[0]//21), eye[0])
    img.paste(eye[0], (img.size[0] - int(img.size[0]//4.55), img.size[0]//21), eye[0])
    img.paste(eye[0], (img.size[0]//21, img.size[0] - int(img.size[0]//4.55)), eye[0])

    _logo = Image.open("card_png_generator/asset/logo.png").resize((600, 200))
    logo = Image.new("RGBA", (_logo.size[0] + 42, _logo.size[1] + 42), "#ffffffff")
    ldraw = ImageDraw.Draw(logo)
    for i in range(_logo.size[0]):
        for j in range(_logo.size[1]):
            ldraw.point((i+21, j+21), "#ffffff00")
            ldraw.point((i+21, j+21), "#002366ff" if _logo.getpixel((i, j))[0] == 255 else "#ffffffff")

    cx = (img.size[0] / 2) - (_logo.size[0] / 2) - 20
    cy = (img.size[1] / 2) - (_logo.size[1] / 2) - 20
    img.paste(Image.new("RGBA", logo.size, "white"), (int(cx), int(cy)))
    img.paste(Image.new("RGBA", logo.size, "#ffffff00"), (int(cx), int(cy)))
    img.paste(logo, (int(cx), int(cy)), logo)

    return img


def get_giftcard(card_number: str):
    cd1 = "-".join(card_number)
    data = "umbra.id/gc-v1-r/" + cd1
    qr = generateQrCode(data, 2).resize((1117, 1117))
    
    # card = Image.open("card_png_generator/asset/giftcard_example.png")
    card  = Image.open("card_png_generator/asset/giftcard_canvas.png")

    draw = ImageDraw.Draw(card)
    font = ImageFont.truetype("card_png_generator/asset/Poppins-Light.ttf", 60)

    padx = 0
    for i in "  ".join(card_number):
        draw.text((80+padx, 1294), i, font=font, fill="#DADADA", align="left")
        padx += 30

    card.paste(qr, (120, 108), qr)
    card.save("card.png")

get_giftcard(random_card_number())

