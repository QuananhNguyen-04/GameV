import sdl2
import components
# import entities
# from system import getEntityfromWorld, getComponentfromWorld

class StatusSystem(sdl2.ext.Applicator):
    def __init__(self):
        super().__init__()
        self.componenttypes = (components.State,)
        self.player_list = None
        self.init_state = True
    def process(self, world, componentsets):
        keys = sdl2.keyboard.SDL_GetKeyboardState(None)
        player_comp = world.combined_components([components.AllyComponent, components.Focus, components.Visibility])
        enemy_comp = world.combined_components([components.EnemyComponent, components.Focus, components.Visibility])
        player_comp = sorted(player_comp, key=lambda x: x[0].type)
        # print(player_comp[0])
        
        # print(len(player_comp))
        length = len(player_comp)
        if enemy_comp is not None:
            e_length = len([enemy_comp])
        else :
            e_length = 0
        if length == 0:
            return
        # TODO: Handle player dead case
        focus_new = False
        focus_enemy = False
        for (state,) in componentsets:
            if keys[sdl2.SDL_SCANCODE_Y]:
                try:
                    state.stateList["Focus"] = not state.stateList["Focus"]
                except KeyError:
                    print(KeyError)
                    return
                break

            elif (keys[sdl2.SDL_SCANCODE_1] and length > 0) or self.init_state:
                try:
                    if state.stateList["Player"] != 0 or self.init_state:
                        focus_new = True
                        state.stateList["Player"] = 0
                        for i, player in enumerate(player_comp): 
                            player[1].focused = False
                            if i == 0:
                                player[1].focused = True
                    if self.init_state:
                        self.init_state = False
                except KeyError:
                    print(KeyError)
                    return
                break

            elif keys[sdl2.SDL_SCANCODE_2] and length > 1:
                
                try:
                    if state.stateList["Player"] != 1:
                        focus_new = True
                        state.stateList["Player"] = 1
                        for i, player in enumerate(player_comp): 
                            player[1].focused = False
                            if i == 1:
                                player[1].focused = True
                except KeyError:
                    print(KeyError)
                    return
                break
            elif keys[sdl2.SDL_SCANCODE_3] and length > 2:
                try:
                    if state.stateList["Player"] != 2:
                        focus_new = True
                        state.stateList["Player"] = 2
                        for i, player in enumerate(player_comp): 
                            player[1].focused = False
                            if i == 2:
                                player[1].focused = True
                except KeyError:
                    print(KeyError)
                    return
                break
            elif keys[sdl2.SDL_SCANCODE_0] and e_length > 0:
                try:
                    if state.stateList["Player"] != 99:
                        state.stateList["Player"] = 99
                        for i, enemy in enumerate(list(enemy_comp)): 
                            enemy[1].focused = False
                            if i == 0:
                                focus_new = True
                                focus_enemy = True
                                enemy[1].focused = True
                except KeyError:
                    print(KeyError)
                    return
                break
        if focus_new:
            if focus_enemy:
                for i, player in enumerate(player_comp):
                    player[1].focused = False
            else:
                for i, enemy in enumerate(list(enemy_comp)):
                    enemy[1].focused = False

        # for i, player in enumerate(player_comp + list(enemy_comp)):
        #     print("Viewable: ", player[0].type, player[1].focused, player[2].visible)