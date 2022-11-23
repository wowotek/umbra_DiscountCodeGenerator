import qrcode
from PIL import Image, ImageDraw
import random, time

def random_card_number():
    data = []
    for _ in range(6):
        d = []
        for _ in range(5):
            d.append("0123456789"[random.randint(0, 9)])
        data.append("".join(d))
    
    print(data)
    return " ".join(data)

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
    
    return matrix

def get_eye(size: int, data_color: tuple[int, int, int, int] = (0, 0, 0, 255), bg_color: tuple[int, int, int, int] = (255, 255, 255, 0)):
    s = (size, size)
    img = Image.new("RGBA", s)
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle((0, 0, size, size), radius=size/8, fill=data_color)
    draw.rounded_rectangle((size/8, size/8, size - (size/8), size - (size/8)), radius=size/8, fill=bg_color)
    draw.rounded_rectangle((size/4, size/4, size - (size/4), size - (size/4)), radius=size/8, fill=data_color)

    return img, Image.new("RGBA", s, "white")

def get_data_point(size: int, data: int, color=(0, 0, 0)):
    s = (size, size)
    if data == 0: return Image.new("RGBA", s, (0, 0, 0, 0)), Image.new("RGBA", s, "white")
    img = Image.new("RGBA", s)
    draw = ImageDraw.Draw(img)

    draw.ellipse((0, 0, size, size), (color[0], color[1], color[2], 50))
    draw.ellipse((size/28, size/28, size - (size/28), size - (size/28)), (color[0], color[1], color[2], 120))
    draw.ellipse((size/19, size/19, size - (size/19), size - (size/19)), (color[0], color[1], color[2], 190))
    draw.ellipse((size/ 8, size/ 8, size - (size/ 8), size - (size/ 8)), (color[0], color[1], color[2], 220))
    draw.ellipse((size/ 6, size/ 6, size - (size/ 6), size - (size/ 6)), (color[0], color[1], color[2], 255))

    return img, Image.new("RGBA", s, "white")

while True:
    data = "umbra.id/gcr/" + "".join([hex(int(i)).replace("0x", "").rjust(5, "0") for i in random_card_number().split(" ")])
    qr = qrcode.QRCode(
        version=5,
        error_correction=qrcode.ERROR_CORRECT_H,
        box_size=50,
        border=2
    )
    qr.add_data(data)
    mat = delete_eye([[1 if j else 0 for j in i] for i in qr.get_matrix()])
    qr = qr.make_image()
    img = Image.new("RGBA", qr.size, "white")
    # img.paste(qr)

    m = 50
    y = 5
    for i in range(len(mat)):
        x = 6
        for j in range(len(mat[i])):
            dp = get_data_point(img.size[0]//50, mat[i][j], (0, 0, 0))
            # img.paste(dp[1], (x, y))
            img.paste(dp[0], (x, y), dp[0])
            x = x + int(img.size[0]/41)
        y = y + int(img.size[0]/41)

    ge = get_eye(int(img.size[0]/5.8), "#002366")
    # img.paste(ge[1], (img.size[0]//21, img.size[0]//21))
    img.paste(ge[0], (img.size[0]//21, img.size[0]//21), ge[0])

    # img.paste(ge[1], (img.size[0] - int(img.size[0]//4.55), img.size[0]//21))
    img.paste(ge[0], (img.size[0] - int(img.size[0]//4.55), img.size[0]//21), ge[0])

    # img.paste(ge[1], (img.size[0]//21, img.size[0] - int(img.size[0]//4.55)))
    img.paste(ge[0], (img.size[0]//21, img.size[0] - int(img.size[0]//4.55)), ge[0])

    _logo = Image.open("card_png_generator/logo.png").resize((600, 200))
    logo = Image.new("RGBA", (_logo.size[0] + 42, _logo.size[1] + 42), "#ffffffff")
    ldraw = ImageDraw.Draw(logo)
    for i in range(_logo.size[0]):
        for j in range(_logo.size[1]):
            ldraw.point((i+21, j+21), "#002366ff" if _logo.getpixel((i, j))[0] == 255 else "#ffffffff")
    
    cx = (img.size[0] / 2) - (_logo.size[0] / 2) - 20
    cy = (img.size[1] / 2) - (_logo.size[1] / 2) - 20
    img.paste(logo, (int(cx), int(cy)), logo)

    img.save("orig.png")
    time.sleep(0.7)
