import pygame
from tkinter import Tk
from tkinter import filedialog
import json
import sys

resolution = (800, 600)

background = None

def set_background():
    global background

    image_file_name = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")], initialdir="~")
    if image_file_name == "" or image_file_name == ():
        return
    background = pygame.image.load(image_file_name)
    background.convert_alpha()
    background.fill((255, 255, 255, 125), None, pygame.BLEND_RGBA_MULT)
    background = pygame.transform.scale(background, (edit_area.rect[2] - 50, edit_area.rect[3] - 50))

if "--help" in sys.argv:
    print("\nUsage: python3 b2dEditor.py [--help] [--resolution <selection>]\n\n"
          "--help:       Prints this help text\n"
          "--resolution: Sets application resolution to selected option: \n"
          "     1: 800x600\n"
          "     2: 1200x900\n"
          "     3: 1800x1350\n")
    sys.exit(0)

if "--resolution" in sys.argv:
    resolution_arg = sys.argv[sys.argv.index("--resolution") + 1]
    if resolution_arg == "1": resolution = (800, 600)
    elif resolution_arg == "2": resolution = (1200, 900)
    elif resolution_arg == "3": resolution = (1800, 1350)

shapes = []
current_shape = 0

shapes.append([])

buttons = []

quit = False
selected = None
Tk().withdraw()

def dump_node_json():
    if __name__ == "__main__":
        export_file_name = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")], initialdir="~")
        if export_file_name == "" or export_file_name == ():
            return

    json_file = {}

    rigid_body = {}
    polygons = []

    for i in range(len(shapes)):
        for j in shapes[i]:

            pos_dict = {}

            pos_dict["x"] = j.pos[0] / edit_area.rect[2]
            pos_dict["y"] = j.pos[1] / edit_area.rect[3]
            polygons.append([pos_dict])

    origin_pos = {}
    origin_pos["x"] = origin.pos[0] / edit_area.rect[2]
    origin_pos["y"] = origin.pos[1] / edit_area.rect[3]
    rigid_body["origin"] = origin_pos
    rigid_body["polygons"] = polygons
    rigid_body["circles"] = []
    rigid_body["shapes"] = []
    json_file["rigidBody"] = rigid_body

    if __name__ == "__main__":
        with open(export_file_name, "w") as export_file:
            json.dump(json_file, export_file, indent=2, sort_keys=True)
    else:
        return json_file

button_flag = False

class Button():
    def __init__(self, size, pos, command, text):
        buttons.append(self)
        self.rect = pygame.Rect(pos, size)
        self.command = command
        self.text = text
        self.norm_color = (50, 50, 50)
        self.color = self.norm_color
        self.hover_color = (100, 100, 100)

    def set_color(self, color):
        self.color = color

    def handle_mouse(self, event):
        global button_flag

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.set_color(self.hover_color)
        else:
            self.set_color(self.norm_color)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    if button_flag == False:
                        exec(self.command)
                        button_flag = True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                button_flag = False


# Define Node class
class Node():
    def __init__(self):
        self.norm_color = (0, 0, 200)
        self.select_color = (0, 100, 0)
        self.color = self.norm_color
        self.pos = (0, 0)
        self.rect = None

    def set_pos(self, pos):
        self.pos = pos

    def set_color(self, color):
        self.color = color

class OriginNode():
    def __init__(self):
        self.color = (200, 0, 0)
        self.pos = (0, 0)
        self.rect = None

    def set_pos(self, pos):
        self.pos = pos

    def set_color(self, color):
        self.color = color

class NodeRect():
    def __init__(self):
        self.edge_color = (150, 150, 150)
        self.color = (250, 250, 250)
        self.rect = pygame.Rect(50, 50, resolution[1] - 100, resolution[1] - 100)

    def handle_mouse(self, event):
        global selected

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for nodes in shapes:
                    for i in nodes:
                        # Compare event position to each node's position
                        if i.pos[0] - 5 <= event.pos[0] <= i.pos[0] + 5 and i.pos[1] - 5 <= event.pos[1] <= i.pos[1] + 5:
                        # Set clicked node's color and set it as selected
                            selected = i
                            set_current_shape(shapes.index(nodes))

                if origin.pos[0] - 6 <= event.pos[0] <= origin.pos[0] + 6 and origin.pos[1] - 6 <= event.pos[1] <= origin.pos[1] + 6:
                    selected = origin

                if selected == None:
                    if edit_area.rect.collidepoint(mouse_pos):
                        add_node(event.pos)

            # Check if mouse2 (3 in pygame terms) clicked on node
            elif event.button == 3:
                for nodes in shapes:
                    for i in nodes:
                        # Compare event position to each node's position
                        if i.pos[0] - 5 <= event.pos[0] <= i.pos[0] + 5 and i.pos[1] - 5 <= event.pos[1] <= i.pos[1] + 5:
                        # Remove clicked node
                            nodes.remove(i)

        # Set selected node's position to the mouse's
        elif event.type == pygame.MOUSEMOTION:
            if selected != None:
                if edit_area.rect.collidepoint(mouse_pos):
                    selected.set_pos(event.pos)
                else: selected = None


        # De-select node on mouse1 release
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if selected != None:
                    selected.clicked = False
                selected = None


def set_current_shape(num):
    global current_shape
    current_shape = num

def add_node(pos):
    new_node = Node()
    new_node.set_pos(pos)
    shapes[current_shape].append(new_node)

def add_shape():
    shapes.append([])
    set_current_shape(len(shapes) - 1)

pygame.init()
pygame.font.init()
font = pygame.font.Font(pygame.font.match_font("monospace,ubuntumono,liberationmono"), int(resolution[1] / 40))
disp = pygame.display.set_mode(resolution)
screen = pygame.Surface(resolution)

edit_area = NodeRect()

ticker = pygame.time.Clock()

origin = OriginNode()
origin.set_pos((100, 100))
button_x = resolution[0] / 4
button_y = resolution[1] / 16

open_image = Button((button_x, button_y), (resolution[0] - button_x, button_y), "set_background()", "Set Background Image")
save = Button((button_x, button_y), (resolution[0] - button_x, button_y * 2.1), "dump_node_json()", "Save JSON")
add_obj = Button((button_x, button_y), (resolution[0] - button_x, button_y * 3.2), "add_shape()", "Add Object")

while not quit:

    ticker.tick(24)
    # Clear the screen
    screen.fill((200, 200, 200))

    mouse_pos = pygame.mouse.get_pos()

    # Handle inputs
    for event in pygame.event.get():

        edit_area.handle_mouse(event)
        for button in buttons:
            button.handle_mouse(event)
        if event.type == pygame.QUIT:
            quit = True

        # Add node if insert is pressed
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_INSERT:
                add_node((10, 10))

            elif event.key == pygame.K_s:
                dump_node_json()

            elif event.key == pygame.K_n:
                add_shape()


    for button in buttons:
        pygame.draw.rect(screen, button.color, button.rect)
        screen.blit(font.render(button.text, False, (200, 200, 200)), (button.rect[0] + 5, button.rect[1] + button.rect[3] / 3))

    pygame.draw.rect(screen, edit_area.color, edit_area.rect)
    pygame.draw.rect(screen, edit_area.edge_color, edit_area.rect, 2)

    if background != None:
        screen.blit(background, ((0.5 * edit_area.rect.width) - (0.5 * background.get_rect().width) + 50, (0.5 * edit_area.rect.height) - (0.5 * background.get_rect().height) + 50))

    if len(shapes) > 0:
        # Iterate through nodes to draw them
        for j in range(len(shapes)):
            nodes = shapes[j]

            if j != current_shape:
                color = 1
            else:
                color = 0

            for i in range(len(nodes)):
                node = nodes[i]
                # Draw line between current and previous node if node is not the first one
                if i > 0:
                    pygame.draw.line(screen, node.color, node.pos, nodes[i - 1].pos, 2)

                # Draw line between last and first node
                if len(nodes) > 0 and i == len(nodes) - 1:
                    pygame.draw.line(screen, node.color, nodes[len(nodes) - 1].pos, nodes[0].pos, 2)

                # Draw node circles
                if node == selected:
                    pygame.draw.circle(screen, node.color, node.pos, 7)
                else:
                    pygame.draw.circle(screen, node.color, node.pos, 4)
                pygame.draw.circle(screen, node.color, node.pos, 8, 2)

                if node == nodes[len(nodes) - 1]:
                    pygame.draw.line(screen, node.color, (node.pos[0] - 10, node.pos[1] - 1), (node.pos[0] + 9, node.pos[1] - 1), 2)
                    pygame.draw.line(screen, node.color, (node.pos[0] - 1, node.pos[1] - 10), (node.pos[0] - 1, node.pos[1] + 9), 2)


                if color == 1:
                    node.set_color(node.norm_color)
                else:
                    node.set_color(node.select_color)

    if origin == selected:
        pygame.draw.circle(screen, origin.color, origin.pos, 8)
    else:
        pygame.draw.circle(screen, origin.color, origin.pos, 4)
    pygame.draw.circle(screen, origin.color, origin.pos, 8, 2)
    pygame.draw.line(screen, origin.color, (origin.pos[0] - 10, origin.pos[1] - 1), (origin.pos[0] + 9, origin.pos[1] - 1), 2)
    pygame.draw.line(screen, origin.color, (origin.pos[0] - 1, origin.pos[1] - 10), (origin.pos[0] - 1, origin.pos[1] + 9), 2)

    disp.blit(screen, (0, 0))

    # Update display
    pygame.display.update()
