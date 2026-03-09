import os
import pygame
import psutil
import json

class button:
    def __init__(self, text, pos, charsize, font):
        self.text = text
        self.pos = pos
        self.rect = None
        self.pressed = False
        self.font = pygame.font.Font(font, charsize)
        self.timesincelastpress = 15

    def draw(self, surface):
        Text = self.font.render(self.text, True, (0, 200, 50))
        text_rect = Text.get_rect(topleft=(self.pos[0] + 6, self.pos[1]))
        self.rect = pygame.Rect(self.pos[0], self.pos[1], Text.get_width() + 12, Text.get_height())
        surface.blit(Text, text_rect)
        pygame.draw.rect(surface, (0, 200, 50), self.rect, 3)
            
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        
        if self.rect and self.rect.collidepoint(mouse_pos):
            if mouse_pressed[0] and not self.pressed and self.timesincelastpress > 15:
                self.pressed = True
                return True
            elif not mouse_pressed[0]:
                self.pressed = False
                self.timesincelastpress += 1
                if self.timesincelastpress <= 15:
                    self.timesincelastpress = 15  
                    
        return False
            
class txt:
    def __init__(self, text, pos, font, charsize, effect = None):
        self.text = text
        self.pos = pos
        self.font = pygame.font.Font(font, charsize)
        self.effect = effect

    def draw(self, surface):
        Text = self.font.render(self.text, True, (0, 200, 50))
        surface.blit(Text, self.pos)
        if self.effect == "underline":
            pygame.draw.line(surface, (0, 200, 50), (self.pos[0], self.pos[1] + Text.get_height()), (self.pos[0] + Text.get_width(), self.pos[1] + Text.get_height()), 3)

class Holotape:
    def __init__(self, OverlaySurface, font):
        self.PageNum = 0
        self.Surface = OverlaySurface
        self.font = font # Now Font Path Instead Of Font Obj Cause Python Is Stupid
        self.LastPage = None

    def Main(self, Screen):
        Clock = pygame.time.Clock()
        
        global exit, leftbutton, rightbutton
        exit = button("EXIT", (0, 0), 24, self.font)
        leftbutton = button("<", (64, 0), 24, self.font)
        rightbutton = button(">", (456, 0), 24, self.font)

        self.averagecpu = []
        self.averagemem = []
        self.playlistselected = 0
        self.tapeselected = 0
        
        while True:
            for Event in pygame.event.get():
                if Event.type == pygame.QUIT:
                    return "ShutDownOS"

            self.averagecpu.append(psutil.cpu_percent())
            self.averagemem.append(psutil.virtual_memory().percent)
            if len(self.averagecpu) > 30:
                self.averagecpu.pop(0)
            if len(self.averagemem) > 30:
                self.averagemem.pop(0)

            Result = self.draw()
            if Result:
                return Result

            Screen.blit(self.Surface, (0, 0))
            pygame.display.flip()
            Clock.tick(30)
            
        return "ShutDownOS"

    def draw(self):  
        self.Surface.fill((0, 0, 0))
        
        offsetconst = 100
        if self.PageNum == 0:
            txtlist = [
                txt("STAT", (offsetconst, 0), self.font, 24, "underline"),
                txt("INV", (offsetconst + 77, 0), self.font, 24),
                txt("DATA", (offsetconst + 140, 0), self.font, 24),
                txt("MAP", (offsetconst + 217, 0), self.font, 24),
                txt("RADIO", (offsetconst + 280, 0), self.font, 24),
                txt(f"CPU: {sum(self.averagecpu) / len(self.averagecpu):.1f}%", (0, 36), self.font, 20),
                txt(f"RAM : {psutil.virtual_memory().used / (1024 ** 2):.0f}MB/{psutil.virtual_memory().total / (1024 ** 2):.0f}MB", (0, 96), self.font, 20),
                txt(f"RAM % : {sum(self.averagemem) / len(self.averagemem):.1f}%", (0, 66), self.font, 20),
                txt(f"DISK : {psutil.disk_usage('/').used / (1024 ** 3):.2f}GB/{psutil.disk_usage('/').total / (1024 ** 3):.2f}GB", (0, 156), self.font, 20),
                txt(f"DISK % : {psutil.disk_usage('/').percent}%", (0, 126), self.font, 20),
            ]

        elif self.PageNum == 1:
            txtlist = [
                txt("STAT", (offsetconst, 0), self.font, 24),
                txt("INV", (offsetconst + 77, 0), self.font, 24, "underline"),
                txt("DATA", (offsetconst + 140, 0), self.font, 24),
                txt("MAP", (offsetconst + 217, 0), self.font, 24),
                txt("RADIO", (offsetconst + 280, 0), self.font, 24)
            ]
            
            tapelist = [f for f in os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)))) if f.endswith(".py") and f != "pipos.py"]
            upbutton = button("/\\", (0, 36), 24, self.font)
            downbutton = button("\/", (0, 280), 24, self.font)
            load = button("LOAD TAPE", (420, 280), 24, self.font)
            upbutton.draw(self.Surface)
            downbutton.draw(self.Surface)
            load.draw(self.Surface)
            if upbutton.update():
                if self.tapeselected > 0:
                    self.tapeselected -= 1
                else:
                    self.tapeselected = len(tapelist) - 1
            if downbutton.update():
                if self.tapeselected < len(tapelist) - 1:
                    self.tapeselected += 1
                else:
                    self.tapeselected = 0
                    
            if load.update() and len(tapelist) > 0:
                return tapelist[self.tapeselected]
                    
            if len(tapelist) == 0:
                txtlist.append(txt("No Tapes Found", (0, 200), self.font, 20))
            elif len(tapelist) < 6:
                for i, tape in enumerate(tapelist):
                    txtlist.append(txt(tape, (0, 72 + i * 36), self.font, 20))
                    if i == self.tapeselected:
                        txtlist[-1].effect = "underline"
            
        elif self.PageNum == 2:
            txtlist = [
                txt("STAT", (offsetconst, 0), self.font, 24),
                txt("INV", (offsetconst + 77, 0), self.font, 24),
                txt("DATA", (offsetconst + 140, 0), self.font, 24, "underline"),
                txt("MAP", (offsetconst + 217, 0), self.font, 24),
                txt("RADIO", (offsetconst + 280, 0), self.font, 24)
            ]
        elif self.PageNum == 3:
            txtlist = [
                txt("STAT", (offsetconst, 0), self.font, 24),
                txt("INV", (offsetconst + 77, 0), self.font, 24),
                txt("DATA", (offsetconst + 140, 0), self.font, 24),
                txt("MAP", (offsetconst + 217, 0), self.font, 24, "underline"),
                txt("RADIO", (offsetconst + 280, 0), self.font, 24)
            ]
        elif self.PageNum == 4:
            txtlist = [
                txt("STAT", (offsetconst, 0), self.font, 24),
                txt("INV", (offsetconst + 77, 0), self.font, 24),
                txt("DATA", (offsetconst + 140, 0), self.font, 24),
                txt("MAP", (offsetconst + 217, 0), self.font, 24),
                txt("RADIO", (offsetconst + 280, 0), self.font, 24),
                txt("RADIO", (offsetconst + 280, 0), self.font, 24, "underline")
            ]
            
            playlistjsonlist = [f for f in os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "radio/playlists")) if f.endswith(".json")]
            playlistlist = []
            for file in playlistjsonlist:
                with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "radio/playlists", file), "r") as f:
                    data = json.load(f)
                    playlistlist.append((data[0]["name"], data[0]["songlist"]))
            
            if len(playlistlist) == 0:
                txtlist.append(txt("No Playlists Found", (0, 200), self.font, 20))
            elif len(playlistlist) < 6:
                for i, playlist in enumerate(playlistlist):
                    txtlist.append(txt(playlist[0], (0, 72 + i * 36), self.font, 20))
                    if i == self.playlistselected:
                        txtlist[-1].effect = "underline"
            else:
                for i in range(6):
                    txtlist.append(txt(str(playlistlist[self.playlistselected + i][0]), (0, 72 + i * 36), self.font, 20))
                    if i == self.playlistselected:
                        txtlist[-1].effect = "underline"
            
            upbutton = button("/\\", (0, 36), 24, self.font)
            downbutton = button("\/", (0, 280), 24, self.font)
            upbutton.draw(self.Surface)
            downbutton.draw(self.Surface)
            if upbutton.update():
                if self.playlistselected > 0:
                    self.playlistselected -= 1
                    print(self.playlistselected)
                    print("UP")
                else:
                    self.playlistselected = len(playlistlist) - 1
            if downbutton.update():
                if self.playlistselected < len(playlistlist) - 1:
                    self.playlistselected += 1
                    print(self.playlistselected)
                    print("DOWN")
                else:
                    self.playlistselected = 0
            
        for t in txtlist:
                t.draw(self.Surface)

        exit.draw(self.Surface)
        leftbutton.draw(self.Surface)
        rightbutton.draw(self.Surface)
        
        if exit.update():
            return "ShutDownOS"
        
        if leftbutton.update():
            if self.PageNum > 0:
                self.PageNum -= 1
            else:
                self.PageNum = 4
                
        if rightbutton.update():
            if self.PageNum < 4:
                self.PageNum += 1
            else:
                self.PageNum = 0