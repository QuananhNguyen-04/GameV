import sdl2
from sdl2 import ext as ext
import components
# import entities
# from utils import getEntityfromWorld, getComponentfromWorld


class KillSystem(sdl2.ext.Applicator):
    def __init__(self):
        super().__init__()
        self.componenttypes = (
            ext.Sprite,
            components.PlayerComponent,
            components.Health,
            components.Execute,
        )
        self.time_counter = None

    def process(self, world, componentsets):
        time_comp = list(world.get_components(components.Time))[0]
        if not time_comp.allow:
            return
        enemy_list = world.combined_components(
            [ext.Sprite, components.PlayerComponent, components.Health]
        )
        e_rect = sdl2.SDL_Rect(0, 0, 0, 0)
        for sprite, player, health, execute in componentsets:
            if health.health <= 0:
                execute.killable = True
                continue
            player_rect = sdl2.SDL_Rect(
                sprite.x, sprite.y, sprite.size[0], sprite.size[1]
            )

            for e_sprite, ptype, health in enemy_list:
                if ptype.type == player.type:
                    # print("same type")
                    continue
                e_rect.x = e_sprite.x
                e_rect.y = e_sprite.y
                e_rect.w = e_sprite.size[0]
                e_rect.h = e_sprite.size[1]
                if sdl2.SDL_HasIntersection(player_rect, e_rect):
                    health.health -= 1
