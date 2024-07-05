import sdl2.ext as ext
import components

class ToggleVisionSystem(ext.Applicator):

    def __init__(self):
        super().__init__()
        self.componenttypes = (
            components.Focus,
            components.Visibility,
        )

    def process(self, world, componentsets):
        for focus, visibility in componentsets:
            if focus.focused is True:
                visibility.visible = True

            else:
                visibility.visible = False