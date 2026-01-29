import sys, math
try:
    import pygame
    from pygame.locals import *
    pygame.init()
except:
    print("Whoops!\n\nYou don't have pygame properly installed.\nFortunately, you can open Powershell (Windows Key + x), then type\n\npip uninstall pygame\n\nthen\n\nY\n\nand finally\n\npip install --force-reinstall pygame\n\nIf you're using a school computer, you might be concerned about the ability of a student to so easily uninstall and install modules using Powershell.\n\nI am too.\n\nBut, as always, don't hate the player, hate the game.") 
    sys.exit()

screen = pygame.display.set_mode((650, 700), RESIZABLE)
pygame.display.set_caption("Grid")
clock = pygame.time.Clock()
cambria = pygame.font.SysFont("cambriamath", 11)

TILE_WIDTH = 70
TILE_HEIGHT = 70
class ScreenCamera():
    def __init__(self, x = 0, y = 0, zoom = 1):
        self.x = x
        self.y = y
        self.zoom = zoom

    def SetCoords(self, coords):
        self.x = coords[0]
        self.y = coords[1]

    def GetCoords(self):
        return (self.x, self.y)
        
    def Pan(self, dcoords):
        self.x += dcoords[0]
        self.y += dcoords[1]
    
    def Zoom(self, dZoom):
        self.zoom *= dZoom

    def SetZoom(self, zoom):
        self.zoom = zoom

    def GetZoom(self):
        return self.zoom
        
    def ToCameraCoords(self, coords):
        return (coords[0] + self.x, coords[1] + self.y)
    
    def Offset(self, coords):
        return list(map(math.ceil, Multiply(Subtract(coords, (self.x, self.y)), self.zoom)))

    def ApplyZoom(self, NumberList):
        return list(map(math.ceil, Multiply(NumberList, self.zoom)))
    
    def Blit(self, screen, surface):
        pass

    
def Add(List1, List2):
    return [List1[i] + List2[i] for i in range(len(List1))]

def Subtract(List1, List2):
    return [List1[i] - List2[i] for i in range(len(List1))]

def Multiply(List1, Coefficient):
    return [Coefficient * i for i in List1]

def Divide(List1, Divisor):
    return [i / Divisor for i in List1]

def Negate(List1):
    return Multiply(List1, -1)

Camera = ScreenCamera()

running = True
MouseCoords = []
while running:
    screen.fill("#000000")




    if pygame.mouse.get_pressed()[0]:
        if MouseCoords == []:
            MouseCoords = pygame.mouse.get_pos()
            CameraCoords = Camera.GetCoords()
        Camera.SetCoords(Add(Divide(Subtract(MouseCoords, pygame.mouse.get_pos()), Camera.GetZoom()), CameraCoords))
    else:
        MouseCoords = []
        


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEWHEEL:
            TempZoom = Camera.GetZoom()
            Camera.Zoom(1.1 ** event.y)
            Camera.Pan(Subtract(Divide(pygame.mouse.get_pos(), TempZoom), Divide(pygame.mouse.get_pos(), Camera.GetZoom())))
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_EQUALS:
                TempZoom = Camera.GetZoom()
                Camera.Zoom(1.1 ** 4)
                Camera.Pan(Subtract(Divide((screen.get_width() / 2, screen.get_height() / 2), TempZoom), Divide((screen.get_width() / 2, screen.get_height() / 2), Camera.GetZoom())))
            if event.key == pygame.K_MINUS:
                TempZoom = Camera.GetZoom()
                Camera.Zoom(1.1 ** -4)
                Camera.Pan(Subtract(Divide((screen.get_width() / 2, screen.get_height() / 2), TempZoom), Divide((screen.get_width() / 2, screen.get_height() / 2), Camera.GetZoom())))
##        print(Camera.GetCoords())

    for i in range(10):
        for j in range(10):
            pygame.draw.rect(screen, f"#{(i + j) % 2 * 4}0bf{(i + j) % 2 * 4}0", [Camera.Offset((i * TILE_WIDTH, j * TILE_HEIGHT)), Camera.ApplyZoom((TILE_WIDTH, TILE_HEIGHT))])

    
##    pygame.draw.rect(screen, "#00ae00", (Camera.Offset((0, 0)), (TILE_WIDTH * Camera.GetZoom(), TILE_HEIGHT * Camera.GetZoom())))

    pygame.draw.circle(screen, "#ff0000", Camera.Offset((0, 0)), 20 * Camera.GetZoom())

##    pygame.draw.circle(screen, "#0000ff", (screen.get_width() / 2, screen.get_height() / 2), 1)
    
    clock.tick(30)
    pygame.display.flip()
