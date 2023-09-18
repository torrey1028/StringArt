import PySimpleGUI as sg
import io
from PIL import Image, ImageDraw
import math
pi = math.pi


print("hi")

points = 200
radius = 5000

plywood = (234, 213, 186, 255)
yarn1 = (204, 153, 201, 255)
yarn2 = (158, 193, 207, 255)
yarn3 = (158, 224, 158, 255)
yarn4 = (253, 253, 151, 255)
yarn5 = (254, 177, 68, 255)
yarn6 = (255, 102, 99, 255)

colors = ['yarn1', 'yarn2', 'yarn3', 'yarn4', 'yarn5', 'yarn6']
elements = []


def string_to_color(string):
    if string == 'yarn1':
        return yarn1
    elif string == 'yarn2':
        return yarn2
    elif string == 'yarn3':
        return yarn3
    elif string == 'yarn4':
        return yarn4
    elif string == 'yarn5':
        return yarn5
    elif string == 'yarn6':
        return yarn6
    else:
        return yarn1


def color_to_string(color):
    if color == yarn1:
        return 'yarn1'
    elif color == yarn2:
        return 'yarn2'
    elif color == yarn3:
        return 'yarn3'
    elif color == yarn4:
        return 'yarn4'
    elif color == yarn5:
        return 'yarn5'
    elif color == yarn6:
        return 'yarn6'
    else:
        return 'yarn1'


def PointsInCircum(r, n=100):
    return [(math.cos(2*pi/n*x)*r, math.sin(2*pi/n*x)*r) for x in range(0, n)]


class Centered:
    def __init__(self, skip, fill, coords, width=0):
        x = 0
        self.pattern = coords[x]
        exit = False
        while not exit:
            x += skip
            self.pattern += coords[x % len(coords)]
            exit = x % len(coords) == 0
        self.fill = fill
        self.width = width

    def render(self, img):
        img.line(self.pattern, fill=self.fill, width=self.width)

# def Centered(skip, img, fill, coords, width=0):
#   x = 0
#   pattern = coords[x]
#   exit = False
#   while not exit:
#     x += skip
#     pattern += coords[x % len(coords)]
#     exit = x % len(coords) == 0
#   img.line(pattern, fill=fill, width=width)


class Fan:
    def __init__(self, origin, start, stop, fill, coords, width=0):
        self.pattern = []
        for x in range(start, stop):
            self.pattern += coords[origin]
            self.pattern += coords[x]
        self.fill = fill
        self.width = width

    def render(self, img):
        img.line(self.pattern, fill=self.fill, width=self.width)

# def Fan(origin, start, stop, img, fill, coords, width=0):
#   pattern = []
#   for x in range(start, stop):
#      pattern += coords[origin]
#      pattern += coords[x]
#   img.line(pattern, fill=fill, width=width)


class Stripe:
    def __init__(self, start, stop, offset, fill, coords, width=0):
        self.pattern = []
        for x in range(start, stop):
            self.pattern += coords[start + x]
            self.pattern += coords[stop - x + offset]
        self.fill = fill
        self.width = width

    def render(self, img):
        img.line(self.pattern, fill=self.fill, width=self.width)

# def Stripe(start, stop, offset, img, fill, coords, width = 0):
#   pattern = []
#   for x in range(start, stop):
#     pattern += coords[start + x]
#     pattern += coords[stop - x + offset]
#   img.line(pattern, fill=fill, width=width)


class HourGlass:
    class_count = 0

    def __init__(self, start, stop, offset, fill, width=0):
        self.fill = fill
        self.width = width
        self.start = start
        self.stop = stop
        self.offset = offset
        self.id = HourGlass.class_count
        HourGlass.class_count += 1
        self.visible = True

    def render(self, img, coords):
        if not self.visible:
            return
        self.pattern = []
        for x in range(self.start, self.start + self.stop):
            self.pattern += coords[(x) % len(coords)]
            self.pattern += coords[(x + self.offset) % len(coords)]
        img.line(self.pattern, fill=self.fill, width=self.width)

    def get_gui(self):
        return [
            sg.Text("Start:"),
            sg.Input(self.start, key='-START' + str(self.id) +
                     '-', justification='left', size=(5, 1)),
            sg.Text("Size:"),
            sg.Input(self.stop, key='-STOP' + str(self.id) +
                     '-', justification='left', size=(5, 1)),
            sg.Text("Offset:"),
            sg.Input(self.offset, key='-OFFSET' + str(self.id) +
                     '-', justification='left', size=(5, 1)),
            sg.Text("Fill:"),
            sg.Combo(colors, color_to_string(self.fill), key='-FILL' + str(self.id) +
                     '-', readonly=False, size=(5, 1)),
            sg.Text("Width:"),
            sg.Input(self.width, key='-WIDTH' + str(self.id) +
                     '-', justification='left', size=(5, 1)),
            sg.Checkbox("Visible", default=True, key='-VISIBLE' + str(self.id) + '-')
        ]
    
    def get_json(self):
        json = {}
        json["start"] = self.start
        json["stop"] = self.stop
        json["offset"] = self.offset
        json["fill"] = color_to_string(self.fill)
        json["width"] = self.width
        json["visible"] = self.visible
        json["id"] = self.id
        return json

# def HourGlass(start, stop, offset, img, fill, coords, width = 0):
#   pattern = []
#   for x in range(start, stop):
#     pattern += coords[(x) % len(coords)]
#     pattern += coords[(x + offset) % len(coords)]
#   img.line(pattern, fill=fill, width=width)


elements.append(HourGlass(int(points/4) + 10, 20, int(points/6), yarn1, 5))
elements.append(HourGlass(int(points/4), 20, int(points/6) + 20, yarn2, 5))
elements.append(HourGlass(int(points/4) - 10, 20,
                int(points/6) + 40, yarn3, 5))

elements.append(HourGlass(int(points/4) - 10, 20, 100, yarn4, 5))

elements.append(HourGlass(int(points/4) - 10, 20, 130, yarn3, 5))
elements.append(HourGlass(int(points/4) - 20, 20, 150, yarn2, 5))
elements.append(HourGlass(int(points/4) - 30, 20, 170, yarn1, 5))
elements.append(HourGlass(int(points/4) - 30, 20, 175, yarn1, 5))
elements.append(HourGlass(int(points/4) - 30, 20, 180, yarn1, 5))
elements.append(HourGlass(int(points/4) - 30, 20, 185, yarn1, 5))
elements.append(HourGlass(int(points/4) - 30, 20, 190, yarn1, 5))
elements.append(HourGlass(int(points/4) - 30, 20, 195, yarn1, 5))


def CreatePoints(radius, points):
    coordinates = PointsInCircum(radius, points)
    translated = []
    for item in coordinates:
        new_coord = (item[0] + (radius), item[1] + (radius))
        translated.append(new_coord)
    return translated


def DrawCircle(radius, points):
    img = Image.new("RGB", (radius*2, radius*2))
    coords = CreatePoints(radius, points)
    img1 = ImageDraw.Draw(img)
    img1.line(coords, width=0)

    for item in elements:
        item.render(img1, coords)

    return img

# creating new Image object
# img = Image.new("RGB", (radius*2, radius*2))

# # create points
# # coordinates = PointsInCircum(radius, points)
# translated = CreatePoints(radius, points)
# # for item in coordinates:
# #     new_coord = (item[0] + (radius), item[1] + (radius))
# #     translated.append(new_coord)


# # draw circle
# img1 = ImageDraw.Draw(img)
# img1.line(translated, width = 0)

# # create pattern
# # yarn1 = (100, 100, 0, 255)
# # yarn2 = (0, 100, 0, 255)
# # yarn3 = (0, 100, 100, 255)
# # yarn4 = (0, 0, 100, 255)
# # yarn5 = (100, 0, 0, 255)

# # Centered(35, img1, yarn1, translated)
# # Centered(37, img1, yarn2, translated)
# # Centered(39, img1, yarn3, translated)
# # Centered(41, img1, yarn4, translated)
# # Centered(33, img1, yarn5, translated)


# # Fan(5, 65, 85, img1, yarn1, translated)
# # Fan(15, 65, 85, img1, yarn2, translated)
# # Fan(25, 65, 85, img1, yarn3, translated)
# # Fan(35, 65, 85, img1, yarn4, translated)
# # Fan(45, 65, 85, img1, yarn5, translated)
# # Fan(55, 65, 85, img1, yarn6, translated)

# HourGlass(int(points/4) + 10, int((points/4)) + 30, int(points/6), img1, yarn1, translated, 5)
# HourGlass(int(points/4), int((points/4)) + 20, int(points/6) + 20, img1, yarn2, translated, 5)
# HourGlass(int(points/4) - 10, int((points/4)) + 10, int(points/6) + 40, img1, yarn3, translated, 5)

# HourGlass(int(points/4) - 10, int((points/4) + 10), 100, img1, yarn4, translated, 5)

# HourGlass(int(points/4) - 10, int((points/4)) + 10, 130, img1, yarn3, translated, 5)
# HourGlass(int(points/4) - 20, int((points/4)), 150, img1, yarn2, translated, 5)
# HourGlass(int(points/4) - 30, int((points/4)) - 10, 170, img1, yarn1, translated, 5)
# # HourGlass(125, 150, 50, img1, yarn2, translated)

# img.show()


# img = DrawCircle(radius, points)


def get_image(img, resize=None):
    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height/cur_height, new_width/cur_width)
        img = img.resize(
            (int(cur_width*scale), int(cur_height*scale)), Image.Resampling.LANCZOS)
    with io.BytesIO() as bio:
        img.save(bio, format="PNG")
        return bio.getvalue()

def create_config_json():
    json = {}
    json["radius"] = radius
    json["points"] = points
    json["elements"] = []
    for item in elements:
        json["elements"].append(item.get_json())
    return json

def apply_config(config):
    json = eval(config)
    radius = json["radius"]
    points = json["points"]
    for item in json["elements"]:
        index = item["id"]
        elements[index].start = item["start"]
        elements[index].stop = item["stop"]
        elements[index].offset = item["offset"]
        elements[index].fill = string_to_color(item["fill"])
        elements[index].width = item["width"]
        elements[index].visible = item["visible"]
        window['-START' + str(index) + '-'].update(value=item["start"])
        window['-STOP' + str(index) + '-'].update(value=item["stop"])
        window['-OFFSET' + str(index) + '-'].update(value=item["offset"])
        window['-FILL' + str(index) + '-'].update(value=item["fill"])
        window['-WIDTH' + str(index) + '-'].update(value=item["width"])
        window['-VISIBLE' + str(index) + '-'].update(value=item["visible"])
    window['-IMAGE-'].update(data=get_image(DrawCircle(radius,
                                     points), resize=(400, 400)))
    window.refresh()

# def convert_to_bytes(file_or_bytes, resize=None):
#    img = Image.open(file_or_bytes)
# imgdata = convert_to_bytes("PySimpleGUI_logo.png")
title = sg.Text("Hello from PySimpleGUI")
save_btn = sg.Button("Save")
update_btn = sg.Button("Update")
load_btn = sg.Button("Load")
input_txt = sg.Text("Points: ")
input_box = sg.Input(points, key='-POINT-',
                     expand_x=True, justification='left')
image = sg.Image(key='-IMAGE-', data=get_image(DrawCircle(radius,
                 points), resize=(400, 400)), size=(400, 400))


def create_list():
    list = []
    list.append([save_btn, load_btn, update_btn])
    list.append([input_txt, input_box])
    for item in elements:
        list.append(item.get_gui())
    return list


layout = [
    [
        sg.Column(create_list()),
        sg.VSeparator(),
        sg.Column([[image]])
    ]
]

# layout = [
#   elements[0].get_gui(),
# ]

# Create the window
window = sg.Window("String Art Visualizer", layout)


# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the Exit button
    if event == sg.WIN_CLOSED:
        break
    if event == "Save":
        filename = sg.popup_get_file('Save Config', save_as=True)
        if filename:
            open(filename, 'w').write(str(create_config_json()))
    if event == "Load":
        filename = sg.popup_get_file('Load Config')
        if filename:
            config = open(filename, 'r').read()
            apply_config(config)


    if event == "Update":
        if values['-POINT-'][-1] not in ('0123456789'):
            sg.popup("Only digits allowed")
        else:
            for x in range(0, len(elements)):
                item = elements[x]
                item.start = int(values['-START' + str(item.id) + '-'])
                item.stop = int(values['-STOP' + str(item.id) + '-'])
                item.offset = int(values['-OFFSET' + str(item.id) + '-'])
                item.fill = string_to_color(values['-FILL' + str(item.id) + '-'])
                item.width = int(values['-WIDTH' + str(item.id) + '-'])
                item.visible = values['-VISIBLE' + str(item.id) + '-']
            window['-IMAGE-'].update(data=get_image(DrawCircle(radius,
                                     int(values['-POINT-'])), resize=(400, 400)))
    if event == "Resize":
        window.refresh()

window.close()

print("done")
