import sdl2.ext as ext
from sdl2 import SDL_GetTicks
import components

class TimingSystem(ext.Applicator):
    def __init__(self):
        super().__init__()
        self.componenttypes = (components.Time, )
    
    def process(self, world, componentsets):
        for (time, ) in componentsets:
            time.allow = False
            if (SDL_GetTicks() - time.last_logic_time > time.cooldown):
                time.last_logic_time = SDL_GetTicks()
                time.allow = True
