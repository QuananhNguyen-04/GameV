import sdl2
from sdl2 import ext as ext
import components

# ! ERROR IN SPRITE AND SURFACE RENDERER, DELAY INDEFINITELY
class ZoomSystem(ext.Applicator):
    def __init__(self):
        super().__init__()
        self.componenttypes = (components.CameraComponent, components.Zoom, components.Position)

    def process(self, world, componentsets):
        start = sdl2.SDL_GetTicks()

        for (camera_size, zoom, pos) in componentsets:
            if zoom.zoom_level == zoom.default_level:
                # zoom.zoom_level += 1
                pass
                # camera_size.size = (camera_size.width * zoom.zoom_level, camera_size.height * zoom.zoom_level)
