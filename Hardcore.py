import json
from textblob import TextBlob
import xlrd
import pygame
import os
from pygame_textinput import *
import random
from input import *
import romkan

colors = {
    "black":pygame.Color(0, 0, 0),
    "white":pygame.Color(255,255,255),
    "blue":pygame.Color(0,128,255),
    "orange":pygame.Color(255,153,51),
    "red":pygame.Color(204,0,0),
    "salmon":pygame.Color(255,153,153),
    "pink":pygame.Color(255,102,178),
    "yellow":pygame.Color(255,255,0),
    "green":pygame.Color(0,255,0),
    "darkgreen":pygame.Color(0,153,0),
    "darkblue":pygame.Color(0,76,153),
    "lightorange":pygame.Color(255, 204, 253)
}
bgc = colors["salmon"]
(width, height) = (800, 600)

class Button():
    def __init__(self, pos, dim, color, string, text_color, font_size, surface = None):
        self.x, self.y = pos[0], pos[1]
        self.w, self.h = dim[0], dim[1]
        self.ulc, self.brc = (self.x, self.y), (self.x + self.w, self.y + self.h)
        self.string = string
        self.color = color
        self.text_color = text_color
        if surface == None:
            self.surface = pygame.Surface(dim)
        else:
            self.surface = surface

        self.box = boxGen([0, 0, self.w, self.h], self.color, self.surface)
        self.text = textGen((self.w/2, self.h/2), self.text_color, font_size, self.string, self.surface, "sv")
        self.state = "idle"

    def draw(self):
        self.box.drawRect()
        self.text.drawText()

    def update(self):
        if self.state == "idle":
            self.surface.set_alpha(70)
        elif self.state == "focus":
            self.surface.set_alpha(255)
        self.draw()

class boxGen():
    """generates rectangles with a color and a highligh color, for when you are
    hoovering with your mouse on the boxes"""
    def __init__(self, pos_and_dim, color, surface):
        self.x = pos_and_dim[0]
        self.y = pos_and_dim[1]
        self.w = pos_and_dim[2]
        self.h = pos_and_dim[3]
        self.color = color
        self.surface = surface

    def drawRect(self):
        """draws the rectangles"""
        button = pygame.draw.rect(self.surface, self.color, pygame.Rect(self.x, self.y, self.w, self.h))

class textGen():
    """Generates text objects"""
    def __init__(self, pos, color, fontsize, string, surface, la = "sv"):
        self.pos = pos
        self.color = color
        self.surface = surface
        self.fontsize = fontsize
        self.string = string
        self.font = None
        if la != "ja":
            self.font = pygame.font.Font(os.path.join(os.path.dirname(__file__), 'fonts', 'Optima.ttc'), self.fontsize)
        elif la == "ja":
            self.font = pygame.font.Font(os.path.join(os.path.dirname(__file__), 'fonts', 'SourceHanSerif-Regular.otf'), self.fontsize)

    def drawText(self):
        """draws the text on the screen"""
        text = self.font.render(self.string, True, self.color)
        self.surface.blit(text, (self.pos[0] - text.get_width()//2, self.pos[1] - text.get_height()//2))

class Glosor():
    def __init__(self, wb, sheet_index):
        self.wb = wb
        self.sheet = self.wb.sheet_by_index(sheet_index)
        self.data = {self.sheet.row_values(i)[0]:self.sheet.row_values(i)[1] for i in range(len(self.sheet.col_values(0)))}

    def Healthy(self):
        pass

def checkBounds(pos, ulc, brc):
    if (ulc[0] < pos[0] < brc[0]) and (ulc[1] < pos[1] < brc[1]):
        return True
    else:
        return False

def updateScreen(buttons, texts, window, mouse_pos):
    for b in buttons:
        if checkBounds(mouse_pos, b.ulc, b.brc):
            b.state = "focus"
        else:
            b.state = "idle"
        b.update()
        window.blit(b.surface, b.ulc)
    for text in texts:
        text.drawText()

def listOfSheets():
    sheet_names = wb.sheet_names()
    positions = [(100+200*i%3, 100+j*20) for i in range((len(sheet_names)-1)//20+1) for j in range(20)]
    return [Button(positions[i], (200, 20), colors["darkgreen"], sheet_names[i], colors["white"], 18, surface = None) for i in range(len(sheet_names))]

def menu():
    window = pygame.display.set_mode((width, height), pygame.DOUBLEBUF)
    pygame.display.set_caption('Glosövaren')
    clock = pygame.time.Clock()

    title_text = textGen((400,150), colors["red"], 72, "Glosövaren", window, "sv")
    b1 = Button((50, 300), (200,100), colors["blue"], "Skriftligt", colors["black"], 40)
    b2 = Button((300, 300), (200,100), colors["blue"], "Auditivt", colors["black"], 40)
    b3 = Button((550, 300), (200,100), colors["blue"], "Muntligt", colors["black"], 40)
    b4 = Button((50, 250), (300,150), colors["blue"], "Svenska -> Japanska", colors["black"], 30)
    b5 = Button((450, 250), (300,150), colors["blue"], "Japanska -> Svenska", colors["black"], 30)

    buttons = [b1, b2, b3]
    texts = [title_text]

    running = True
    step1 = True
    step2 = False
    step3 = False
    sheet_index = None
    order = None
    start_buttons = [False]*3
    order = [False]*2
    while running:
        mouse_pos = pygame.mouse.get_pos()
        window.fill(bgc)
        clock.tick(60)

        updateScreen(buttons, texts, window, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            if step1:
                if event.type == pygame.MOUSEBUTTONUP and checkBounds(mouse_pos, b1.ulc, b1.brc):
                    step1 = False
                    step2 = True
                    buttons = listOfSheets()
                    texts =[textGen((400, 50), colors["red"], 60, "Välj glosor", window)]
                    start_buttons[0] = True
                elif event.type == pygame.MOUSEBUTTONUP and checkBounds(mouse_pos, b2.ulc, b2.brc):
                    step1 = False
                    step2 = True
                    buttons = listOfSheets()
                    texts =[textGen((400, 50), colors["red"], 60, "Välj glosor", window)]
                    start_buttons[1] = True
                elif event.type == pygame.MOUSEBUTTONUP and checkBounds(mouse_pos, b3.ulc, b3.brc):
                    step1 = False
                    step2 = True
                    buttons = listOfSheets()
                    texts =[textGen((400, 50), colors["red"], 60, "Välj glosor", window)]
                    start_buttons[2] = True
            elif step2:
                for i, b in enumerate(buttons):
                    if event.type == pygame.MOUSEBUTTONUP and checkBounds(mouse_pos, b.ulc, b.brc):
                        sheet_index = i
                        buttons = [b4, b5]
                        step2 = False
                        step3 = True
                        texts =[textGen((400, 50), colors["red"], 60, "Välj översättningsriktning", window)]
                        break
            elif step3:
                if event.type == pygame.MOUSEBUTTONUP and checkBounds(mouse_pos, b4.ulc, b4.brc):
                    order[0] = True
                    running = False
                elif event.type == pygame.MOUSEBUTTONUP and checkBounds(mouse_pos, b5.ulc, b5.brc):
                    order[1] = True
                    running = False

        pygame.display.flip()
    print(start_buttons)

    if start_buttons[0] == True:
        if order[0] == True:
            input_ja(sheet_index)
        elif order[1] == True:
            input_sv(sheet_index)
    elif start_buttons[1] == True:
        pass
    elif start_buttons[2] == True:
        pass

def input_sv(sheet_index):
    window = pygame.display.set_mode((width, height), pygame.DOUBLEBUF)
    pygame.display.set_caption('Skriftligt test – input på Japanska')
    clock = pygame.time.Clock()

    glosor = Glosor(wb, sheet_index)
    sv, ja = random.choice(list(glosor.data.items()))
    texts = [textGen((400,150), colors["red"], 72, ja, window, "ja")]
    textinput = TextInput(font_family=os.path.join(os.path.dirname(__file__), 'fonts', 'Optima.ttc'))

    correct = None
    running = True
    score = 0
    tries = 0
    while running:

        if correct == False:
            wrong(window, clock, mouse_pos)
        elif correct == True:
            right(window, clock, mouse_pos)
        correct = None

        mouse_pos = pygame.mouse.get_pos()
        window.fill(bgc)
        clock.tick(60)

        updateScreen([], texts, window, mouse_pos)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        if textinput.update(events):
            answer = textinput.get_text()
            if answer == sv and len(glosor.data) > 1:
                del glosor.data[sv]
                sv, ja = random.choice(list(glosor.data.items()))
                texts = [textGen((400,150), colors["red"], 72, ja, window, "ja")]
                textinput.clear_text()
                window.blit(textinput.get_surface(), (400-0.5*textinput.get_surface().get_width(), 300))
                score += 1
                correct = True
            elif answer == sv and len(glosor.data) == 1:
                running = False
                textinput.clear_text()
                window.blit(textinput.get_surface(), (400-0.5*textinput.get_surface().get_width(), 300))
                score += 1
                right(window, clock, mouse_pos)
                break
            else:
                correct = False
                sv, ja = random.choice(list(glosor.data.items()))
                texts = [textGen((400,150), colors["red"], 72, ja, window)]
                textinput.clear_text()

        tries += 1

        window.blit(textinput.get_surface(), (400-0.5*textinput.get_surface().get_width(), 300))

        pygame.display.flip()
    menu()

def input_ja(sheet_index):
    window = pygame.display.set_mode((width, height), pygame.DOUBLEBUF)
    pygame.display.set_caption('Skriftligt test – input på Japanska')
    clock = pygame.time.Clock()

    glosor = Glosor(wb, sheet_index)
    sv, ja = random.choice(list(glosor.data.items()))
    texts = [textGen((400,150), colors["red"], 72, sv, window)]
    textinput = TextInput(font_family=os.path.join(os.path.dirname(__file__), 'fonts', 'SourceHanSerif-Regular.otf'), language = "ja")

    correct = None
    running = True
    score = 0
    tries = 0
    while running:

        if correct == False:
            wrong(window, clock, mouse_pos)
        elif correct == True:
            right(window, clock, mouse_pos)
        correct = None

        mouse_pos = pygame.mouse.get_pos()
        window.fill(bgc)
        clock.tick(60)

        updateScreen([], texts, window, mouse_pos)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        if textinput.update(events):
            answer = textinput.get_text()
            if answer == ja and len(glosor.data) > 1:
                del glosor.data[sv]
                sv, ja = random.choice(list(glosor.data.items()))
                texts = [textGen((400,150), colors["red"], 72, sv, window)]
                textinput.clear_text()
                window.blit(textinput.get_surface(), (400-0.5*textinput.get_surface().get_width(), 300))
                score += 1
                correct = True
            elif answer == ja and len(glosor.data) == 1:
                running = False
                score += 1
                textinput.clear_text()
                window.blit(textinput.get_surface(), (400-0.5*textinput.get_surface().get_width(), 300))
                right(window, clock, mouse_pos)
                break
            else:
                correct = False
                sv, ja = random.choice(list(glosor.data.items()))
                texts = [textGen((400,150), colors["red"], 72, sv, window)]
                textinput.clear_text()
            tries += 1

        window.blit(textinput.get_surface(), (400-0.5*textinput.get_surface().get_width(), 300))

        pygame.display.flip()
    menu()

def wrong(window, clock, mouse_pos):
    c = colors["red"]
    texts = [textGen((400,150), colors["black"], 80, "FEL!", window), textGen((500,400), colors["black"], 20, "du suger", window)]
    time = 5
    dt = 0.1
    while time >= 0:
         window.fill(c)
         clock.tick(60)
         time -= dt
         updateScreen([], texts, window, mouse_pos)
         events = pygame.event.get()
         for event in events:
             if event.type == pygame.QUIT:
                 running = False

         pygame.display.flip()

def right(window, clock, mouse_pos):
    c = colors["green"]
    texts = [textGen((400,150), colors["black"], 80, "RÄTT!", window)]
    time = 5
    dt = 0.1
    while time >= 0:
         window.fill(c)
         clock.tick(60)
         time -= dt
         updateScreen([], texts, window, mouse_pos)
         events = pygame.event.get()
         for event in events:
             if event.type == pygame.QUIT:
                 running = False

         pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    path = os.path.join(os.path.dirname(__file__),"excelfiles","/ord.xlsx")
    wb = xlrd.open_workbook(path)
    menu()
