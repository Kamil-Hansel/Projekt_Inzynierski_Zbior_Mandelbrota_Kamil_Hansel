from PIL import Image,ImageDraw, ImageFont
import colorsys
import imageio.v2 as imageio
import time
import numpy as np
import matplotlib.pyplot as plt
import openpyxl

width = 1920
x = -0.65
y = 0
xRange = 3.4
aspectRatio = 4 / 3
height = round(width / aspectRatio)
yRange = xRange / aspectRatio

minX = x - xRange / 2
maxX = x + xRange / 2
minY = y - yRange / 2
maxY = y + yRange / 2

img = Image.new('RGB', (width, height), color='black')
pixels = img.load()



def powerColor(distance, exp, const, scale):
    color = distance ** exp
    rgb = colorsys.hsv_to_rgb(const + scale * color, 1 - 0.6 * color, 0.9)
    return tuple(round(i * 255) for i in rgb)


def mandelbrot(c, max_iter):
    n = 0
    z = 0
    while n < max_iter:
        if abs(z) > 2:
            print("wieksze niz 2" + str(z))
            # complex_numbers.append(z)
            # break
        if z in visited:
            print("z należy do zbioru liczb odwiedzonych" + "f" + str(n) + "=" + str(z))
            #break
        complex_numbers.append(z)
        print("fz" + "=" + str(z))
        visited.add(z)
        z = z * z + c
        n += 1
    return n


def on_click(event):
    global c
    if event.button == 1:
        x, y = event.xdata, event.ydata
        if x is not None and y is not None:
            real_part = x
            imag_part = y
            c = complex(real_part, imag_part)
            print(f"Clicked coordinates: Real={real_part}, Imag={imag_part}")
            plt.close()


while 1<3:
    print("1.Wygeneruj zdjecie")
    print("2.Wygeneruj gif")
    print("3.Wygeneruj zdjecie z punktami")
    print("4.Wygeneruj zdjecie julii")
    tryb=int(input("podaj tryb:"))
    if tryb==1:
        precision = int(input("podaj precyzje:"))
        start_time = time.time()
        for row in range(height):
            for col in range(width):
                x = minX + col * xRange / width
                y = maxY - row * yRange / height
                oldX = x
                oldY = y
                for i in range(precision + 1):
                    a = x * x - y * y
                    b = 2 * x * y
                    x = a + oldX
                    y = b + oldY
                    if x * x + y * y > 4:
                        break
                if i < precision:
                    distance = (i + 1) / (precision + 1)
                    rgb = powerColor(distance, 0.2, 0.27, 1.0)
                    pixels[col, row] = rgb

        print("czas potrzebny na wygenerowanie outputu to: %s sekund" % round((time.time() - start_time), 3))
        print("ukończono output " + str(precision))
        img.save('tryb1/tryb1_precyzja' + str(precision) + '.png')
        break
    elif tryb==2:
        images = []
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Execution Times"
        sheet.append(["Precision", "Execution Time (seconds)"])

        precision_values = []
        execution_times = []
        precision = int(input("podaj precyzje:"))
        for k in range(1, precision+1):
            start_time = time.time()
            precision = k
            for row in range(height):
                for col in range(width):
                    x = minX + col * xRange / width
                    y = maxY - row * yRange / height
                    oldX = x
                    oldY = y
                    for i in range(precision + 1):
                        a = x * x - y * y
                        b = 2 * x * y
                        x = a + oldX
                        y = b + oldY
                        if x * x + y * y > 4:
                            break
                    if i < precision:
                        distance = (i + 1) / (precision + 1)
                        rgb = powerColor(distance, 0.2, 0.27, 1.0)
                        pixels[col, row] = rgb
            execution_time = round((time.time() - start_time), 3)
            precision_values.append(k)
            execution_times.append(execution_time)
            print("czas potrzebny na wygenerowanie outputu to: %s sekund" % round((time.time() - start_time), 3))
            print("ukończono output " + str(k))
            img.save('tryb2/tryb2_precyzja' + str(k) + '.png')
            images.append(imageio.imread('tryb2/tryb2_precyzja' + str(k) + '.png'))
            k += 1

        imageio.mimsave('tryb2/tryb2.gif', images)
        for i in range(len(precision_values)):
            sheet.append([precision_values[i], execution_times[i]])

        workbook.save("tryb2/execution_times.xlsx")
        break
    elif tryb==3:
        xRange = 6
        yRange = xRange / aspectRatio
        minX = x - xRange / 2
        maxX = x + xRange / 2
        minY = y - yRange / 2
        maxY = y + yRange / 2

        jednostka = width / (xRange)
        img = Image.open('tryb3/tryb3.png')

        draw = ImageDraw.Draw(img)

        center = (width - 2.35 * jednostka, width / (aspectRatio * 2))
        radius = 2 * jednostka

        circle_color = (255, 255, 255)
        x1 = center[0] - radius
        y1 = center[1] - radius
        x2 = center[0] + radius
        y2 = center[1] + radius


        draw.ellipse([x1, y1, x2, y2], outline=circle_color)

        axes_color = (255, 255, 255)


        pixels = img.load()


        x_axis_position = round((0 - minX) / xRange * width)
        y_axis_position = round((0 - minY) / yRange * height)


        for col in range(width):
            pixels[col, y_axis_position] = axes_color


        for row in range(height):
            pixels[x_axis_position, row] = axes_color

        draw = ImageDraw.Draw(img)


        font = ImageFont.truetype("arial.ttf", 12)


        x_title = "X-axis"
        y_title = "Y-axis"
        x_title_position = (width - 120, height - 30)
        y_title_position = (10, 10)


        draw.text(x_title_position, x_title, fill=axes_color, font=font)
        draw.text(y_title_position, y_title, fill=axes_color, font=font)


        x_step = xRange / width
        y_step = yRange / height


        for i in range(-35, 24):
            x_number = i * 0.1
            x_number_position = int((x_number - minX) / xRange * width)
            draw.text((x_number_position, height - 20), f"{x_number:.1f}", fill=axes_color, font=font)

        for i in range(-22, 22):
            y_number = i * 0.1
            y_number_position = height - int((y_number - minY) / yRange * height)
            draw.text((5, y_number_position), f"{y_number:.1f}", fill=axes_color, font=font)

        img.save('tryb3/tryb31.png')
        a = float(input("Podaj liczbę rzeczywistą: "))
        b = float(input("Podaj liczbę zespoloną: "))
        c = complex(a, b)
        max_iter = int(input("Podaj maksymalną liczbę iteracji: "))
        max_iter += 1

        complex_numbers = []
        visited = set()
        start_time = time.time()
        mandelbrot(c, max_iter)
        complex_numbers.pop(0)






        img = Image.open('tryb3/tryb31.png')
        for i in range(len(complex_numbers)):
            if i==0:
                fill_color = "red"
                radius=4
            else:
                fill_color="white"
                radius = 3

            draw = ImageDraw.Draw(img)

            points = [
                (
                    width - 2.35 * jednostka + np.real(complex_numbers[i]) * jednostka,
                    width / (aspectRatio * 2) - np.imag(complex_numbers[i]) * jednostka),
            ]

            point_radius = radius
            for point_x, point_y in points:
                draw.ellipse(
                    [point_x - point_radius, point_y - point_radius, point_x + point_radius, point_y + point_radius],
                    fill=fill_color)

        draw = ImageDraw.Draw(img)

        line_color = "white"

        for i in range(len(complex_numbers) - 1):
            point1 = (
                width - 2.35 * jednostka + np.real(complex_numbers[i]) * jednostka,
                width / (aspectRatio * 2) - np.imag(complex_numbers[i]) * jednostka,
            )
            point2 = (
                width - 2.35 * jednostka + np.real(complex_numbers[i + 1]) * jednostka,
                width / (aspectRatio * 2) - np.imag(complex_numbers[i + 1]) * jednostka,
            )
            draw.line([point1, point2], fill=line_color, width=2)
        img.save('tryb3/tryb32.png')
        img = Image.open('tryb3/tryb32.png')
        for i in range(len(complex_numbers)):
            if i==0:
                fill_color = "red"
                radius=4
            else:
                fill_color="white"
                radius = 3
            draw = ImageDraw.Draw(img)

            font = ImageFont.truetype("DejaVuSans.ttf", 18)

            subscript = chr(0x2081 + i)

            points = [
                (
                    width - 2.35 * jednostka + np.real(complex_numbers[i]) * jednostka,
                    width / (aspectRatio * 2) - np.imag(complex_numbers[i]) * jednostka,
                    f'z{subscript}' + "=" + str(
                        complex(round(complex_numbers[i].real, 2), round(complex_numbers[i].imag, 2)))),
            ]
            point_radius = 3
            for point_x, point_y, label_text in points:
                draw.ellipse(
                    [point_x - point_radius, point_y - point_radius, point_x + point_radius, point_y + point_radius],
                    fill="white")

                if abs(point_x) < 1920 or abs(point_y) < 1440:
                    label_position = (point_x + 10, point_y)
                    draw.text(label_position, label_text, fill="white", font=font)


        draw = ImageDraw.Draw(img)
        img.save('tryb3/tryb33.png')

        img = Image.open('tryb3/tryb32.png')

        img.show()
        break
    elif tryb==4:
        real_part = float(input("Podaj część rzeczywistą: "))
        imag_part = float(input("Podaj część zespoloną: "))


        def julia_set(real, imag, width, height, xmin, xmax, ymin, ymax, max_iter):
            result = np.zeros((width, height))

            x = np.linspace(xmin, xmax, width)
            y = np.linspace(ymin, ymax, height)
            X, Y = np.meshgrid(x, y)
            Z = X - 1j * Y

            for i in range(max_iter):
                Z = Z ** 2 + complex(real, imag)
                mask = np.abs(Z) < 1000
                result += mask

            return result


        def plot_julia_set(real, imag, width, height, xmin, xmax, ymin, ymax, max_iter):
            julia = julia_set(real, imag, width, height, xmin, xmax, ymin, ymax, max_iter)

            plt.imshow(julia, extent=(xmin, xmax, ymin, ymax), cmap='hot', interpolation='bilinear')
            plt.axis('off')
            plt.title(f'Julia Set (c = {real} + {imag}i)')
            plt.savefig('tryb5/tryb5.png')
            plt.show()

        width, height = 800, 800
        xmin, xmax = -2, 2
        ymin, ymax = -2, 2
        max_iter = 100

        plot_julia_set(real_part, imag_part, width, height, xmin, xmax, ymin, ymax, max_iter)
        break
    else:
        print("wybrano zly tryb")