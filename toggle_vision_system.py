import sdl2.ext as ext
import components

class ToggleVisionSystem(ext.Applicator):

    def __init__(self):
        super().__init__()
        self.componenttypes = (
            components.Focus,
            components.Visibility,
            components.Team
        )

    def process(self, world, componentsets):
        global_state = list(world.get_components(components.State))[0]
        state_dict = global_state.stateList
        team = state_dict["Team"]
        for focus, visibility, pteam in componentsets:
            if pteam.team == team:
                visibility.visible = True
            else:
                visibility.visible = False