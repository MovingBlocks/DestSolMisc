import pygame
from tkinter import Tk
from tkinter import filedialog
import json
import sys

resolution = (800, 600)
return_json = ""
background = None


class Button:
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

        # Check if mouse is over button, and set color accordingly
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.set_color(self.hover_color)
        else:
            self.set_color(self.norm_color)

        # Check if mouse1 is pressed on button, and set state
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    if not button_flag:
                        exec(self.command)
                        button_flag = True

        # Reset state on mouse1 release
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                button_flag = False


class Node:
    def __init__(self):
        self.norm_color = (0, 0, 200)
        self.origin_color = (200, 0, 0)
        self.select_color = (0, 100, 0)
        self.color = self.norm_color
        self.pos = (0, 0)
        self.rect = None

    def set_pos(self, pos):
        self.pos = pos

    def set_color(self, color):
        self.color = color


class NodeRect:
    def __init__(self):
        self.edge_color = (150, 150, 150)
        self.color = (250, 250, 250)
        self.rect = pygame.Rect(50, 50, resolution[1] - 100, resolution[1] - 100)

    def handle_mouse(self, event):
        global selected

        # Check if mouse1 is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for nodes in shapes:
                    for node in nodes:
                        # Compare event position to each node's position
                        if node.pos[0] - 5 <= event.pos[0] <= node.pos[0] + 5 and node.pos[1] - 5 <= event.pos[1] <= node.pos[1] + 5:
                            # Set clicked node's color and set it as selected
                            selected = node
                            set_current_shape(shapes.index(nodes))

                # Set origin as selected if it is clicked
                if origin.pos[0] - 6 <= event.pos[0] <= origin.pos[0] + 6 and origin.pos[1] - 6 <= event.pos[1] <= origin.pos[1] + 6:
                    selected = origin

                # Add a new node if user clicks ouside of other ones
                if not selected:
                    if edit_area.rect.collidepoint(mouse_pos):
                        add_node(event.pos)

            # Check if mouse2 (3 in pygame terms) clicked on node
            elif event.button == 3:
                for nodes in shapes:
                    for node in nodes:
                        # Compare event position to each node's position
                        if node.pos[0] - 5 <= event.pos[0] <= node.pos[0] + 5 and node.pos[1] - 5 <= event.pos[1] <= node.pos[1] + 5:
                            # Remove clicked node
                            nodes.remove(node)

        # Set selected node's position to the mouse position
        elif event.type == pygame.MOUSEMOTION:
            if selected:
                if edit_area.rect.collidepoint(mouse_pos):
                    selected.set_pos(event.pos)

                else:
                    selected = None

        # Reset selection on mouse release
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if selected:
                    selected.clicked = False

                selected = None


# Check for any arguments
if "--help" in sys.argv or "-h" in sys.argv:
    print("\nUsage: python3 b2dEditor.py [--help] [--resolution <selection>]\n\n"
          "--help, -h:       Prints this help text\n"
          "--resolution, -r: Sets application resolution to selected option: \n"
          "     1: 800x600\n"
          "     2: 1200x900\n"
          "     3: 1800x1350\n")
    sys.exit(0)

if "--resolution" in sys.argv or "-r" in sys.argv:
    if "-r" in sys.argv:
        resolution_arg = sys.argv[sys.argv.index("-r") + 1]

    else:
        resolution_arg = sys.argv[sys.argv.index("--resolution") + 1]

    if resolution_arg == "1": resolution = (800, 600)
    elif resolution_arg == "2": resolution = (1200, 900)
    elif resolution_arg == "3": resolution = (1800, 1350)


shapes = [[]]
buttons = []
current_shape = 0
quit = False
selected = None
Tk().withdraw()

def draw_nodes(screen):
    if len(shapes) > 0:
        # Iterate through shapes
        for shape in range(len(shapes)):
            nodes = shapes[shape]

            # Set current shape color to green
            if shape != current_shape:
                color = 1
            else:
                color = 0

            # Iterate through nodes and draw them
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

                # Draw indicator lines on last node circle
                if node == nodes[len(nodes) - 1]:
                    pygame.draw.line(screen, node.color, (node.pos[0] - 10, node.pos[1] - 1), (node.pos[0] + 9, node.pos[1] - 1), 2)
                    pygame.draw.line(screen, node.color, (node.pos[0] - 1, node.pos[1] - 10), (node.pos[0] - 1, node.pos[1] + 9), 2)

                # Set node colors
                if color == 1:
                    node.set_color(node.norm_color)

                else:
                    node.set_color(node.select_color)

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

def set_background():
    """
    Sets a background image for the editor.
    """
    global background

    # Open a png image to apply as the background and process the alpha
    image_file_name = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")], initialdir="~")
    if image_file_name == "" or image_file_name == ():
        return
    background = pygame.image.load(image_file_name)
    background.convert_alpha()
    background.fill((255, 255, 255, 125), None, pygame.BLEND_RGBA_MULT)

    # Set the background
    background = pygame.transform.scale(background, (edit_area.rect[2] - 50, edit_area.rect[3] - 50))

def dump_node_json():
    """
    Dumps and exports the nodes into a JSON.

    Returns:
        A JSON object if application is not ran as stand-alone, otherwise returns nothing.
    """
    global return_json, quit

    json_file = {}
    rigid_body = {}
    polygons = []

    # Iterate through shapes and append them to polygons
    for shape in range(len(shapes)):
        pos_root_list = []
        # Iterate through nodes in each shape and add their positions to a list
        for node in shapes[shape]:

            pos_dict = {}

            pos_dict["x"] = node.pos[0] / edit_area.rect[2]
            pos_dict["y"] = node.pos[1] / edit_area.rect[3]

            pos_root_list.append(pos_dict)

        polygons.append(pos_root_list)

    origin_pos = {}

    # Set all the JSON values
    origin_pos["x"] = origin.pos[0] / edit_area.rect[2]
    origin_pos["y"] = origin.pos[1] / edit_area.rect[3]
    rigid_body["origin"] = origin_pos
    rigid_body["polygons"] = polygons
    rigid_body["circles"] = []
    rigid_body["shapes"] = []
    json_file["rigidBody"] = rigid_body

    if __name__ == "__main__":
        # Select the file to export
        export_file_name = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")], initialdir="~")
        if export_file_name == "" or export_file_name == ():
            return

        # Open the export file and dump the JSON
        with open(export_file_name, "w") as export_file:
            json.dump(json_file, export_file, indent=2, sort_keys=True)
    else:
        # Return the JSON if name is not main
        return_json = json_file
        quit = True

def load_node_json():
    """
    Loads nodes and shapes from a JSON file.
    """
    # Select the file to import
    import_file_name = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")], initialdir="~")
    if import_file_name == "" or import_file_name == ():
        return

    # Open the export file and load the JSON
    with open(import_file_name, "r") as import_file:
        json_file = json.load(import_file)

    # Iterate through polygons in JSON and add a new shape for each one
    for polygon in json_file["rigidBody"]["polygons"]:
        # Create all nodes in each polygon
        for node in polygon:
            x = int(node["x"] * edit_area.rect[2] + edit_area.rect[0])
            y = int(node["y"] * edit_area.rect[3] + edit_area.rect[1])
            add_node((x, y))
        add_shape()

    origin.set_pos((int(json_file["rigidBody"]["origin"]["x"] * edit_area.rect[2]), int(json_file["rigidBody"]["origin"]["y"] * edit_area.rect[3])))

def handle_inputs():
    # Handle inputs
    for event in pygame.event.get():

        edit_area.handle_mouse(event)
        for button in buttons:
            button.handle_mouse(event)
        if event.type == pygame.QUIT:
            quit = True

        elif event.type == pygame.KEYDOWN:
            # Save if s is pressed
            if event.key == pygame.K_s:
                dump_node_json()

            # Load if l is pressed
            elif event.key == pygame.K_l:
                load_node_json()

            # Add shape if insert is pressed
            elif event.key == pygame.K_INSERT:
                add_shape()

def run():
    global edit_area, origin, mouse_pos, quit, button_flag

    pygame.init()
    pygame.font.init()
    font = pygame.font.Font(pygame.font.match_font("monospace,ubuntumono,liberationmono"), int(resolution[1] / 40))
    disp = pygame.display.set_mode(resolution)
    screen = pygame.Surface(resolution)
    edit_area = NodeRect()
    ticker = pygame.time.Clock()
    origin = Node()
    origin.set_color(origin.origin_color)
    origin.set_pos((int(0.5 * edit_area.rect[2] + edit_area.rect[0]), int(0.5 * edit_area.rect[3] + edit_area.rect[1])))
    button_flag = False
    button_x = resolution[0] / 4
    button_y = resolution[1] / 16
    Button((button_x, button_y), (resolution[0] - button_x, button_y), "set_background()", "Set Ship Image")
    Button((button_x, button_y), (resolution[0] - button_x, button_y * 2.1), "dump_node_json()", "Export JSON")
    Button((button_x, button_y), (resolution[0] - button_x, button_y * 3.2), "load_node_json()", "Import JSON")
    Button((button_x, button_y), (resolution[0] - button_x, button_y * 4.3), "add_shape()", "Add Object")
    Button((button_x, button_y), (resolution[0] - button_x, resolution[1] - button_y * 2), "exit()", "Exit")

    # Main loop
    while not quit:
        # Limit FPS to 24 to minimize CPU usage
        ticker.tick(24)

        # Clear the screen
        screen.fill((200, 200, 200))

        mouse_pos = pygame.mouse.get_pos()

        handle_inputs()

        # Draw all buttons
        for button in buttons:
            pygame.draw.rect(screen, button.color, button.rect)
            screen.blit(font.render(button.text, False, (200, 200, 200)), (button.rect[0] + 5, button.rect[1] + button.rect[3] / 3))

        # Draw help text
        help_position_x = resolution[0] * 0.75
        help_position_y = resolution[1] - button_y * 3.1
        pygame.draw.rect(screen, (50, 50, 50), ((help_position_x, help_position_y), (button_x, font.get_height() * 2.1)))
        screen.blit(font.render("Mouse1: add node", False, (200, 200, 200)), (help_position_x + 5, help_position_y))
        screen.blit(font.render("Mouse2: remove node", False, (200, 200, 200)), (help_position_x + 5, help_position_y + font.get_height()))

        # Draw editing square
        pygame.draw.rect(screen, edit_area.color, edit_area.rect)
        pygame.draw.rect(screen, edit_area.edge_color, edit_area.rect, 2)

        # Draw background image
        if background:
            screen.blit(background, ((0.5 * edit_area.rect.width) - (0.5 * background.get_rect().width) + 50, (0.5 * edit_area.rect.height) - (0.5 * background.get_rect().height) + 50))

        draw_nodes(screen)

        # Draw the origin circle
        if origin == selected:
            pygame.draw.circle(screen, origin.color, origin.pos, 8)

        else:
            pygame.draw.circle(screen, origin.color, origin.pos, 4)

        pygame.draw.circle(screen, origin.color, origin.pos, 8, 2)
        pygame.draw.line(screen, origin.color, (origin.pos[0] - 10, origin.pos[1] - 1), (origin.pos[0] + 9, origin.pos[1] - 1), 2)
        pygame.draw.line(screen, origin.color, (origin.pos[0] - 1, origin.pos[1] - 10), (origin.pos[0] - 1, origin.pos[1] + 9), 2)

        # Blit display surface onto actual screen
        disp.blit(screen, (0, 0))

        # Update display
        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    run()
