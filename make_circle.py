import PySimpleGUI as sg
import io
from PIL import Image, ImageDraw
import math
pi = math.pi

# global variables -> should definitely be wrapped in a class at some point
points = 200 # nails around the circle
radius = 5000 # in pixels
# 36 inches = 10000 pixels, 1 inch = 277.777 pixels
scale_factor = 277.777
elements = []

# available colors
plywood = (234, 213, 186, 255)
yarn1 = (204, 153, 201, 255)
yarn2 = (158, 193, 207, 255)
yarn3 = (158, 224, 158, 255)
yarn4 = (253, 253, 151, 255)
yarn5 = (254, 177, 68, 255)
yarn6 = (255, 102, 99, 255)
colors = ['yarn1', 'yarn2', 'yarn3', 'yarn4', 'yarn5', 'yarn6']

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

# Different image features, each should implement: 
# 1. render() function which takes an image as a parameter and draws itself on 
#    the image
# 2. get_gui() function which returns a list of gui elements to be displayed 
#    in the window that the user can use to change the object
# 3. get_json() function which returns a json object representing the object
#    which can be used to save an object to and load an object from a file
# 
# Currently only the HourGlass class is implememented properly

class Centered:
    def __init__(self, skip, fill, element_count, width=0):
        self.fill = fill
        self.width = width
        self.skip = skip
        self.yarn_len = 0
        self.visible = True
        self.id = element_count

    def render(self, img, coords):
        self.yarn_len = 0
        if not self.visible:
            return
        x = 0
        pattern = coords[x]
        exit = False
        while not exit:
            x += self.skip
            pattern += coords[x % len(coords)]
            exit = x % len(coords) == 0

        img.line(pattern, fill=self.fill, width=self.width)

    def get_gui(self):
        return [
            sg.Text("Skip:"),
            sg.Input(self.skip, key='-SKIP-cen' + str(self.id) +
                     '-', justification='left', size=(5, 1)),
            sg.Text("Fill:"),
            sg.Combo(colors, color_to_string(self.fill), key='-FILL-cen' + str(self.id) +
                     '-', readonly=False, size=(5, 1)),
            sg.Text("Width:"),
            sg.Input(self.width, key='-WIDTH-cen' + str(self.id) +
                     '-', justification='left', size=(5, 1)),
            sg.Checkbox("Visible", default=True, key='-VISIBLE-cen' + str(self.id) + '-')
        ]
    
    def get_json(self):
        json = {}
        json["skip"] = self.skip
        json["fill"] = color_to_string(self.fill)
        json["width"] = self.width
        json["visible"] = self.visible
        return json

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

class Stripe:
    def __init__(self, start, stop, offset, fill, coords, width=0):
        self.pattern = []
        for x in range(start, stop):
            self.pattern += coords[start + x]
            self.pattern += coords[stop - x + offset]
        self.fill = fill
        self.width = width
        for x in range(0, len(self.pattern) - 1):
            self.yarn_len += math.dist(self.pattern[x], self.pattern[(x + 1)])


    def render(self, img):
        img.line(self.pattern, fill=self.fill, width=self.width)

class HourGlass:
    def __init__(self, start, stop, offset, fill, element_count, width=0):
        self.fill = fill
        self.width = width
        self.start = start
        self.stop = stop
        self.offset = offset
        self.id = element_count
        self.visible = True
        self.yarn_len = 0

    def render(self, img, coords):
        self.yarn_len = 0
        if not self.visible:
            return
        self.pattern = []
        for x in range(self.start, self.start + self.stop):
            self.pattern += coords[(x) % len(coords)]
            self.pattern += coords[(x + self.offset) % len(coords)]

        for x in range(0, len(self.pattern) - 3, 2):
            self.yarn_len += math.dist([self.pattern[x], self.pattern[(x + 1)]], [self.pattern[(x + 2)], self.pattern[(x + 3)]])

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


# Generate points around a circle, this list is later translated from being 
# centered around (0,0) to being centered around (radius, radius) 
def PointsInCircum(r, n=100):
    return [(math.cos(2*pi/n*x)*r, math.sin(2*pi/n*x)*r) for x in range(0, n)]

# Creates list of points centered around (radius, radius) used by visual
# elements as coordinates to draw themselves
def CreatePoints(radius, points):
    coordinates = PointsInCircum(radius, points)
    translated = []
    for item in coordinates:
        new_coord = (item[0] + (radius), item[1] + (radius))
        translated.append(new_coord)
    return translated

# Draws the circle and all visual elements in the global elements list on it
def DrawCircle(radius, points):
    img = Image.new("RGB", (radius*2, radius*2))
    coords = CreatePoints(radius, points)
    img1 = ImageDraw.Draw(img)
    img1.line(coords, width=0)

    for item in elements:
        item.render(img1, coords)

    return img

# Converts an image to bytes so that it can be displayed in the window
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

# Creates a json object representing the current state of the program
def create_config_json():
    json = {}
    json["radius"] = radius
    json["points"] = points
    json["elements"] = []
    for item in elements:
        json["elements"].append(item.get_json())
    return json

# Applies a json object to the current state of the program
def apply_config(config):
    json = eval(config)
    radius = json["radius"]
    points = json["points"]
    for item in json["elements"]:
        index = item["id"]
        if type(elements[index]) is HourGlass:
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
        elif type(elements[index]) is Centered:
            elements[index].skip = item["skip"]
            elements[index].fill = string_to_color(item["fill"])
            elements[index].width = item["width"]
            elements[index].visible = item["visible"]
            window['-SKIP-cen' + str(index) + '-'].update(value=item["skip"])
            window['-FILL-cen' + str(index) + '-'].update(value=item["fill"])
            window['-WIDTH-cen' + str(index) + '-'].update(value=item["width"])
            window['-VISIBLE-cen' + str(index) + '-'].update(value=item["visible"])
    window['-IMAGE-'].update(data=get_image(DrawCircle(radius,
                                     points), resize=(400, 400)))
    window.refresh()

def get_yarn_list():
    yarn_len_list = {}
    for color in colors:
        yarn_len_list[color] = 0
    for item in elements:
        yarn_len_list[color_to_string(item.fill)] += item.yarn_len

    render_list = []
    for item in yarn_len_list:
        render_list.append(sg.Text(item + ": " + str(yarn_len_list[item]/scale_factor), key='-YARN' + item + '-'))

    return render_list

def update_yarn_list():
    yarn_len_list = {}
    for color in colors:
        yarn_len_list[color] = 0
    for item in elements:
        yarn_len_list[color_to_string(item.fill)] += item.yarn_len

    for item in yarn_len_list:
        window['-YARN' + item + '-'].update(item + ": " + str(yarn_len_list[item]/scale_factor))

# creates visual layout for virst column of the window
def create_list():
    list = []
    list.append([save_btn, load_btn, update_btn])
    list.append([input_txt, input_box])
    for item in elements:
        list.append(item.get_gui())
    list.append(get_yarn_list())
    return list

# add visual elements to the global elements list
element_count = 0
elements.append(HourGlass(int(points/4) + 10, 20, int(points/6), yarn1, element_count, 5))
element_count += 1
elements.append(HourGlass(int(points/4), 20, int(points/6) + 20, yarn2, element_count, 5))
element_count += 1
elements.append(HourGlass(int(points/4) - 10, 20,
                int(points/6) + 40, yarn3, element_count, 5))
element_count += 1
elements.append(HourGlass(int(points/4) - 10, 20, 100, yarn4, element_count, 5))
element_count += 1
elements.append(HourGlass(int(points/4) - 10, 20, 130, yarn3, element_count, 5))
element_count += 1
elements.append(HourGlass(int(points/4) - 20, 20, 150, yarn2, element_count, 5))
element_count += 1
elements.append(HourGlass(int(points/4) - 30, 20, 170, yarn1, element_count, 5))
element_count += 1
elements.append(HourGlass(int(points/4) - 30, 20, 175, yarn1, element_count, 5))
element_count += 1
elements.append(HourGlass(int(points/4) - 30, 20, 180, yarn1, element_count, 5))
element_count += 1
elements.append(HourGlass(int(points/4) - 30, 20, 185, yarn1, element_count, 5))
element_count += 1
elements.append(HourGlass(int(points/4) - 30, 20, 190, yarn1, element_count, 5))
element_count += 1
elements.append(HourGlass(int(points/4) - 30, 20, 195, yarn1, element_count, 5))
element_count += 1
elements.append(Centered(15, yarn5, element_count, 5))
element_count += 1
elements.append(Centered(15, yarn5, element_count, 5))
element_count += 1
elements.append(Centered(15, yarn5, element_count, 5))
element_count += 1
elements.append(Centered(15, yarn5, element_count, 5))
element_count += 1
elements.append(Centered(15, yarn5, element_count, 5))
element_count += 1
elements.append(Centered(15, yarn5, element_count, 5))
element_count += 1

save_btn = sg.Button("Save")
update_btn = sg.Button("Update")
load_btn = sg.Button("Load")
input_txt = sg.Text("Points: ")
input_box = sg.Input(points, key='-POINT-',
                     expand_x=True, justification='left')
image = sg.Image(key='-IMAGE-', data=get_image(DrawCircle(radius,
                 points), resize=(400, 400)), size=(400, 400))

# layout used by the window
layout = [
    [
        sg.Column(create_list()),
        sg.VSeparator(),
        sg.Column([[image]])
    ]
]

# Create the window
window = sg.Window("String Art Visualizer", layout)

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window 
    if event == sg.WIN_CLOSED:
        break
    # Save current configuration to a file
    if event == "Save":
        filename = sg.popup_get_file('Save Config', save_as=True)
        if filename:
            open(filename, 'w').write(str(create_config_json()))
    # Load configuration from a file
    if event == "Load":
        filename = sg.popup_get_file('Load Config')
        if filename:
            config = open(filename, 'r').read()
            apply_config(config)
    # Update the image with the new configuration
    if event == "Update":
        if values['-POINT-'][-1] not in ('0123456789'):
            sg.popup("Only digits allowed")
        else:
            for x in range(0, len(elements)):
                item = elements[x]
                if type(item) is HourGlass:
                    item.start = int(values['-START' + str(item.id) + '-'])
                    item.stop = int(values['-STOP' + str(item.id) + '-'])
                    item.offset = int(values['-OFFSET' + str(item.id) + '-'])
                    item.fill = string_to_color(values['-FILL' + str(item.id) + '-'])
                    item.width = int(values['-WIDTH' + str(item.id) + '-'])
                    item.visible = values['-VISIBLE' + str(item.id) + '-']
                elif type(item) is Centered:
                    item.skip = int(values['-SKIP-cen' + str(item.id) + '-'])
                    item.fill = string_to_color(values['-FILL-cen' + str(item.id) + '-'])
                    item.width = int(values['-WIDTH-cen' + str(item.id) + '-'])
                    item.visible = values['-VISIBLE-cen' + str(item.id) + '-']
                    
            window['-IMAGE-'].update(data=get_image(DrawCircle(radius,
                                     int(values['-POINT-'])), resize=(400, 400)))
            update_yarn_list()
    if event == "Resize":
        window.refresh()

window.close()
