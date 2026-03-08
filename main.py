import sys
import os
import importlib.util
import pygame

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HOLOTAPE_DIR = os.path.join(BASE_DIR, "holotape")

def LoadApp(Path, Screen, OverlaySurface):
    try:
        Spec = importlib.util.spec_from_file_location("holotape", Path)
        Mod = importlib.util.module_from_spec(Spec)
        Spec.loader.exec_module(Mod)
        App = Mod.Holotape(OverlaySurface, BASE_DIR + "\monofonto.ttf")
        WhatNext = App.Main(Screen)
        return WhatNext
    except Exception as e:
        print(f"holotape load failed: {e}")
        return "error"

def main():
    global font
    pygame.init()
    Screen = pygame.display.set_mode((480, 320))
    OverlaySurface = pygame.Surface((480, 320))
    font = pygame.font.Font(BASE_DIR + "\monofonto_fixed.ttf", 36)

    print("Welcome To PipOS")
    WhatNext = LoadApp(os.path.join(HOLOTAPE_DIR, "pipos.py"), Screen, OverlaySurface)
    while WhatNext != "ShutDownOS":
        if WhatNext == "error":
            print("An error occurred while loading the app. Returning to main menu.")
            WhatNext = LoadApp(os.path.join(HOLOTAPE_DIR, "pipos.py"), Screen, OverlaySurface)
        else:
            WhatNext = LoadApp(os.path.join(HOLOTAPE_DIR, WhatNext), Screen, OverlaySurface)
            
    pygame.quit()

if __name__ == "__main__":
    main()
    if pygame.get_init():
        pygame.quit()
    sys.exit("Shutting Down PipOS, Bye!")