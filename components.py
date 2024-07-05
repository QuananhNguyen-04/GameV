# COMPONENTS CLASSES: STORE DATA
import sdl2


class Position(object):
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y


class Health(object):
    def __init__(self, h) -> None:
        print("max health", h)
        self.health = h
        self.max_health = h


class Damage(object):
    def __init__(self, d=2) -> None:
        self.damage = d


class Focus(object):
    def __init__(self, focus=False) -> None:
        self.focused = focus


class Execute(object):
    def __init__(self, killed=False) -> None:
        self.killable = killed


class Velocity:
    def __init__(self) -> None:
        self.vx = 0
        self.vy = 0


class CameraComponent:
    def __init__(self, w, h) -> None:
        self.size = (w, h)

    @property
    def width(self):
        return self.size[0]

    @property
    def height(self):
        return self.size[1]


class Visibility:
    def __init__(self, vi=True, block=False) -> None:
        self.visible = vi
        self.block = block


class State:
    def __init__(self, state_key, state_value) -> None:
        self.stateList = dict()
        for key, value in zip(state_key, state_value):
            self.stateList.update({key: value})


class Fog:
    def __init__(self, w, h, sw, sh) -> None:
        self.surface = sdl2.SDL_CreateRGBSurfaceWithFormat(
            0, w, h, 32, sdl2.SDL_PIXELFORMAT_RGBA32
        )
        # print(type(self.surface))
        self.x = 0
        self.y = 0
        self.pixfmt = self.surface.contents.format
        self.rect = sdl2.SDL_Rect(0, 0, w, h)
        self.semi_transparent = sdl2.SDL_MapRGBA(self.pixfmt, 0, 0, 0, 128)
        sdl2.SDL_FillRect(
            self.surface,
            self.rect,
            self.semi_transparent,
        )

    def reload(self, x, y, sw, sh):
        # if self.surface.contents.w != sw or self.surface.contents.h != sh:
        #     self.surface = sdl2.SDL_CreateRGBSurfaceWithFormat(
        #         0, sw, sh, 32, sdl2.SDL_PIXELFORMAT_RGBA32
        #     )
        self.rect.x = x
        self.rect.y = y
        sdl2.SDL_FillRect(
            self.surface,
            self.rect,
            self.semi_transparent,
        )


class ObjComponent:
    def __init__(self, type) -> None:
        self.type = type


class TileComponent(ObjComponent):
    def __init__(self, type) -> None:
        super().__init__(type)
        self.class_name = "Tile"

class PlayerComponent(ObjComponent):
    def __init__(self, type, factory, spriteLists) -> None:
        super().__init__(type)
        self.team = type
        self.factory = factory
        self.spriteLists = spriteLists


class AllyComponent(PlayerComponent):
    def __init__(self, type, factory, spriteLists) -> None:
        super().__init__(type, factory, spriteLists)


class EnemyComponent(PlayerComponent):
    def __init__(self, type, factory, spriteLists) -> None:
        super().__init__(type, factory, spriteLists)


class Ray:
    def __init__(self, pos, num, radius) -> None:
        self.pos = (
            pos.position[0] + pos.size[0] // 2,
            pos.position[1] + pos.size[1] // 2,
        )
        self.n = 360 // num
        self.radius = radius
        self.end_points = None
        # self.precomputed_angles = [math.radians(angle) for angle in range(0, 360, n)]


class Zoom:
    def __init__(self) -> None:
        self.zoom_level = 1
        self.zoom_level_max = 3
        self.default_level = 1
        self.zoom_level_min = 1
        self.zoom_step = 1


class SpriteList:
    def __init__(self, spriteLists, factory) -> None:
        self.slists = []
        for sprite in spriteLists:
            imgsprite = factory.from_image(sprite)
            self.slists.append(imgsprite)

        # self.spriteLists = spriteLists

class Path:
    def __init__(self, path: list = None) -> None:
        self.path = path
        self.current_pos = 0
    def assign_path(self, path = None):
        self.path = path
        self.current_pos = 0
    def next(self, sprite):
        # assert self.path is not None
        if self.path is None:
            return None
        # for item in self.path:
        #     print(item.area, end=" ")
        # print('')
        current_sprite = self.path[self.current_pos]
        # if self.current_pos != len(self.path) - 1:
        #     next_sprite = self.path[self.current_pos + 1]
        
        # if (sprite.x != current_sprite.x and sprite.y != current_sprite.y):
        #     return current_sprite
            # if sprite.x == current_sprite.x:
            #     if current_sprite.y <= sprite.y < next_sprite.y:
            #         self.current_pos += 1
            #     elif current_sprite.y >= sprite.y > next_sprite.y:
            #         self.current_pos += 1
            #     return self.path[self.current_pos]
            # elif sprite.y == current_sprite.y:
            #     if current_sprite.x <= sprite.x < next_sprite.x:
            #         self.current_pos += 1
            #     elif current_sprite.x >= sprite.x > next_sprite.x:
            #         self.current_pos += 1
            #     return self.path[self.current_pos]
        if sprite.area != current_sprite.area:
            return current_sprite
        else:
            self.current_pos += 1
            
        if self.current_pos < len(self.path):
            # print(type(self.path[self.current_pos]))
            return self.path[self.current_pos]
        else:
            self.path = None
            return None
