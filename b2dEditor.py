import pygame
from tkinter import Tk
from tkinter import filedialog
import json

shapes = []
current_shape = 0

shapes.append([])

selected = None

quit = False
selected = None
Tk().withdraw()

def dump_node_json():
    export_file_name = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")], initialdir="~")
    if export_file_name == "" or export_file_name == ():
        return

    json_file = []

    rigidBody = {}
    polygons = []

    for i in range(len(shapes)):
        json_file.append([])
        for j in shapes[i]:

            pos_dict = {}

            pos_dict["x"] = j.pos[0]
            pos_dict["y"] = j.pos[1]
            polygons.append([pos_dict])

    rigidBody["polygons"] = polygons
    json_file.append(rigidBody)

    with open(export_file_name, "w") as export_file:
        json.dump(json_file, export_file, indent=2, sort_keys=True)

# Define Node class
class Node():
    def __init__(self):
        self.norm_color = (0, 0, 200)
        self.select_color = (0, 100, 0)
        self.clicked = False
        self.color = self.norm_color
        self.pos = (0, 0)
        self.rect = None

    def set_pos(self, pos):
        self.pos = pos

    def set_color(self, color):
        self.color = color
        #print("INFO: Set node ", nodes.index(self), " color to ", self.color)

class NodeRect():
    def __init__(self):
        self.edge_color = (150, 150, 150)
        self.color = (250, 250, 250)
        self.rect = pygame.Rect(50, 50, screen.get_rect()[2] - 100, screen.get_rect()[3] - 100)

    def handle_mouse(self, event):
        global selected

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for nodes in shapes:
                    for i in nodes:
                        # Compare event position to each node's position
                        if i.pos[0] - 5 <= event.pos[0] <= i.pos[0] + 5 and i.pos[1] - 5 <= event.pos[1] <= i.pos[1] + 5:
                        # Set clicked node's color and set it as selected
                            i.clicked = True
                            selected = i
                            set_current_shape(shapes.index(nodes))

                if selected == None:
                    if edit_area.rect.collidepoint(mouse_pos):
                        add_node(event.pos)

            # Check if mouse2 (3 in pygame terms) clicked on node
            elif event.button == 3:
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

pygame.init()
disp = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
screen = pygame.Surface((800, 600), pygame.RESIZABLE)

edit_area = NodeRect()

while not quit:

    # Clear the screen
    screen.fill((200, 200, 200))

    mouse_pos = pygame.mouse.get_pos()

    # Handle inputs
    for event in pygame.event.get():

        edit_area.handle_mouse(event)
        if event.type == pygame.QUIT:
            quit = True

        # Add node if insert is pressed
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_INSERT:
                add_node((10, 10))

            elif event.key == pygame.K_s:
                dump_node_json()

            elif event.key == pygame.K_n:
                shapes.append([])
                #print(current_shape)
                set_current_shape(len(shapes) - 1)
                #print(current_shape)

        elif event.type == pygame.VIDEORESIZE:
            print("wasd")
            disp = pygame.display.set_mode(event.size, pygame.RESIZABLE)
            screen = pygame.transform.scale(screen, event.size)

    #print(len(shapes))

    pygame.draw.rect(screen, edit_area.color, edit_area.rect)
    pygame.draw.rect(screen, edit_area.edge_color, edit_area.rect, 2)

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

                if color == 1:
                    node.set_color(node.norm_color)
                else:
                    node.set_color(node.select_color)

    disp.blit(screen, (0, 0))

    # Update display
    pygame.display.update()
