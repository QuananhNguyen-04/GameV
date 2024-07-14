import sdl2.ext as ext
import sdl2
import components
import entities
# from __init import PLAYER_SPEED
from utils import getEntityfromWorld, getComponentfromWorld

# from quadtree import Quadtree
import init
from init import SCREEN_HEIGHT, SCREEN_WIDTH

class CameraSystem(ext.Applicator):
    def __init__(self):
        super().__init__()
        self.componenttypes = (
            components.CameraComponent,
            components.Position,
            components.Velocity,
        )
        self.player_list = None
        self.global_state = None
        self.camera = None

    def camera_movement(self, keys, pos, vel, camera, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        mouse_border = 100
        if keys[sdl2.SDL_SCANCODE_LEFT] or (mouse_x > 0 and mouse_x < mouse_border):
            if mouse_x < mouse_border and mouse_x > 0:
                vel.vx -= 16
            vel.vx -= 16
        elif keys[sdl2.SDL_SCANCODE_RIGHT] or (mouse_x < camera.size[0] and mouse_x > camera.size[0] - mouse_border):
            if mouse_x > camera.size[0] - mouse_border and mouse_x < camera.size[0]:
                vel.vx += 16
            vel.vx += 16
        if keys[sdl2.SDL_SCANCODE_UP] or (mouse_y > 0 and mouse_y < mouse_border):
            if mouse_y < mouse_border and mouse_y > 0:
                vel.vy -= 16
            vel.vy -= 16
        elif keys[sdl2.SDL_SCANCODE_DOWN] or (mouse_y < camera.size[1] and mouse_y > camera.size[1] - mouse_border):
            if mouse_y > camera.size[1] - mouse_border and mouse_y < camera.size[1]:
                vel.vy += 16
            vel.vy += 16
        if vel.vx == 0:
            pass
        elif vel.vx < 0:
            vel.vx = max(vel.vx, pos.x * -1)
        elif vel.vx > 0:
            vel.vx = (
                min(pos.x + camera.size[0] + vel.vx, init.GAME_WIDTH)
                - pos.x
                - camera.size[0]
            )

        if vel.vy == 0:
            pass
        elif vel.vy < 0:
            vel.vy = max(vel.vy, pos.y * -1)
        elif vel.vy > 0:
            vel.vy = (
                min(pos.y + camera.size[1] + vel.vy, init.GAME_HEIGHT)
                - pos.y
                - camera.size[1]
            )
        pos.x += vel.vx
        pos.y += vel.vy
    # ! focus on enemy entities for debug, invest gameplay
    def process(self, world, componentsets):
        # start = sdl2.SDL_GetTicks()
        # GAME_WIDTH = GAME_WIDTH
        # GAME_HEIGHT = __init.GAME_HEIGHT
        keys = sdl2.SDL_GetKeyboardState(None)
        mouse_pos = sdl2.ext.mouse_coords()
        if self.player_list is None:
            self.player_list = getEntityfromWorld(world, entities.PlayerEntity)
            self.player_list = sorted(
                self.player_list,
                key=lambda x: getComponentfromWorld(
                    world, x, components.PlayerComponent
                ).type,
            )
        if self.global_state is None:
            self.global_state = getEntityfromWorld(world, entities.GlobalState)[0]

        stateLists = getComponentfromWorld(
            world, self.global_state, components.State
        ).stateList

        if self.camera is None:
            self.camera = getEntityfromWorld(world, entities.CameraEntity)[0]

        camera = getComponentfromWorld(world, self.camera, components.CameraComponent)
        pos = getComponentfromWorld(world, self.camera, components.Position)
        vel = getComponentfromWorld(world, self.camera, components.Velocity)
        vel.vx, vel.vy = 0, 0
        sprite = None
        state = None
        try:
            state = stateLists["Focus"]
        except KeyError:
            print(KeyError)
        if keys[sdl2.SDL_SCANCODE_SPACE] or state is True:
            player_comp = world.combined_components(
                [ext.Sprite, components.Focus]
            )
            for (player, focus) in player_comp:
                if focus.focused:
                    sprite = player
            # print("player:", sprite.position)
            centerx = sprite.position[0] + sprite.size[0] // 2
            centery = sprite.position[1] + sprite.size[1] // 2
            # print("center:", centerx, centery)

            screenx = centerx - SCREEN_WIDTH // 2
            screeny = centery - SCREEN_HEIGHT // 2
            # print("screen:", screenx, screeny)

            pos.x = max(min(screenx, init.GAME_WIDTH - camera.size[0]), 0)
            pos.y = max(min(screeny, init.GAME_HEIGHT - camera.size[1]), 0)

        else:
            # self.camera_movement(keys, pos, vel, camera, mouse_pos)
            if keys[sdl2.SDL_SCANCODE_LEFT] or mouse_pos[0] in range(0, 30):
                if mouse_pos[0] in range(0, 30):
                    vel.vx -= 32
                vel.vx -= 16
            if keys[sdl2.SDL_SCANCODE_RIGHT] or mouse_pos[0] in range(
                camera.size[0] - 30, camera.size[0]
            ):
                if mouse_pos[0] in range(camera.size[0] - 30, camera.size[0]):
                    vel.vx += 32
                vel.vx += 16
            if keys[sdl2.SDL_SCANCODE_UP] or mouse_pos[1] in range(0, 30):
                if mouse_pos[1] in range(0, 30):
                    vel.vy -= 32
                vel.vy -= 16
            if keys[sdl2.SDL_SCANCODE_DOWN] or mouse_pos[1] in range(
                camera.size[1] - 30, camera.size[1]
            ):
                if mouse_pos[1] in range(camera.size[1] - 30, camera.size[1]):
                    vel.vy += 32
                vel.vy += 16
            if vel.vx == 0:
                pass
            elif vel.vx < 0:
                vel.vx = max(vel.vx, pos.x * -1)
            elif vel.vx > 0:
                vel.vx = (
                    min(pos.x + camera.size[0] + vel.vx, init.GAME_WIDTH)
                    - pos.x
                    - camera.size[0]
                )

            if vel.vy == 0:
                pass
            elif vel.vy < 0:
                vel.vy = max(vel.vy, pos.y * -1)
            elif vel.vy > 0:
                vel.vy = (
                    min(pos.y + camera.size[1] + vel.vy, init.GAME_HEIGHT)
                    - pos.y
                    - camera.size[1]
                )
            pos.x += vel.vx
            pos.y += vel.vy

        # for (sprite,) in componentsets:
        #     sprite.position = (sprite.position[0] - vel.vx, sprite.position[1] - vel.vy)

        # print("Camera", sdl2.SDL_GetTicks() - start, "ms")


class InputSystem(sdl2.ext.Applicator):
    def __init__(self):
        super().__init__()
        self.componenttypes = (
            components.PlayerComponent,
            ext.Sprite,
            components.Velocity,
            components.Focus,
            components.Path
        )
        # self.start_time = sdl2.SDL_GetTicks()


    def process(self, world, componentsets):
        time_comp = list(world.get_components(components.Time))[0]
        if not time_comp.allow:
            return
        # dt = (sdl2.SDL_GetTicks() - self.start_time)
        # self.start_time = sdl2.SDL_GetTicks()
        keys = sdl2.keyboard.SDL_GetKeyboardState(None)
        # if self.player_list is None:
        #     self.player_list = getEntityfromWorld(world, entities.PlayerEntity)
        #     self.player_list = sorted(
        #         self.player_list,
        #         key=lambda x: getComponentfromWorld(
        #             world, x, components.PlayerComponent
        #         ).type,
        #     )
        
        speed = 16
        for player, sprite, velocity, focus, path in componentsets:
            velocity.vx = 0
            velocity.vy = 0
            if focus.focused:
                key_press = False
                if keys[sdl2.SDL_SCANCODE_W]:
                    key_press = True
                    velocity.vy = -speed
                elif keys[sdl2.SDL_SCANCODE_S]:
                    key_press = True
                    velocity.vy = speed
                elif keys[sdl2.SDL_SCANCODE_A]:
                    key_press = True
                    velocity.vx = -speed
                elif keys[sdl2.SDL_SCANCODE_D]:
                    key_press = True
                    velocity.vx = speed
                if key_press:
                    path.assign_path()
            # if 
            if path is None:
                continue
            next_pos = path.next(sprite)
            if next_pos is None:
                continue
            dx, dy = next_pos
            
            # sprite.x = next_pos.x
            # dx = 0 if (next_pos.x == sprite.x) else 1 if (next_pos.x > sprite.x) else -1
            # # sprite.y = next_pos.y
            # dy = 0 if (next_pos.y == sprite.y) else 1 if (next_pos.y > sprite.y) else -1
            # print((dx, dy))
            velocity.vx += dx * speed
            velocity.vy += dy * speed

class MovementSystem(sdl2.ext.Applicator):
    def __init__(self):
        super().__init__()
        self.componenttypes = (
            components.PlayerComponent,
            ext.Sprite,
            components.Velocity,
        )
        self.time_counter = None

    def process(self, world, componentsets):
        time_comp = list(world.get_components(components.Time))[0]
        if not time_comp.allow:
            return
        for player, sprite, velocity in componentsets:
            direction = (
                "left" if velocity.vx < 0 else "none" if velocity.vx == 0 else "right"
            )
            direction = (
                "up" if velocity.vy < 0 else direction if velocity.vy == 0 else "down"
            )
            if direction == "none":
                continue
            sprite.x += int(velocity.vx) #* 16 // 16
            sprite.y += int(velocity.vy) #* 16 // 16 
            pos = sprite.position
            print(pos)
            if direction == "left" or direction == "right":
                sprite = player.factory.from_image(player.spriteLists[direction])
                sprite.position = pos[0], pos[1]
                entity = world.get_entities(player)
                entity[0].sprite = sprite
            # break

        # print("Movement", sdl2.SDL_GetTicks() - start, "ms")


class CollisionSystem(sdl2.ext.Applicator):
    def __init__(self, quadtree):
        super().__init__()
        self.componenttypes = (
            components.PlayerComponent,
            ext.Sprite,
            components.Velocity,
        )
        self.quadtree = quadtree
        # self.tiles = None
        self.obs_list = None
        self.grass_list = None

    def process(self, world, componentset):
        time_comp = list(world.get_components(components.Time))[0]
        if not time_comp.allow:
            return
        start = sdl2.SDL_GetTicks()
        # camera = getEntityfromWorld(world, entities.CameraEntity)[0]
        # camera_pos = getComponentfromWorld(world, camera, components.Position)
        # camera_comp = getComponentfromWorld(world, camera, components.CameraComponent)

        player_rect = sdl2.SDL_Rect(0, 0, 0, 0)
        tile_rect = sdl2.SDL_Rect(0, 0, 0, 0)
        for obj, sprite, velocity in componentset:
            if velocity.vx == 0 and velocity.vy == 0:
                continue
            # FIXME: need to fix this
            new_x = sprite.x + velocity.vx
            new_y = sprite.y + velocity.vy

            #* overflow case
            if new_x < 0:  # and camera_pos.x == 0:
                sprite.x = 0
                velocity.vx = 0
            if new_y < 0:  # and camera_pos.y == 0:
                velocity.vy = sprite.y = 0
            if (
                new_x + sprite.size[0] > init.GAME_WIDTH  # camera_comp.width
                # and camera_pos.x + camera_comp.width == __init.GAME_WIDTH
            ):
                velocity.vx = 0
                sprite.x = init.GAME_WIDTH - sprite.size[0]
            if (
                new_y + sprite.size[1] > init.GAME_HEIGHT  # camera_comp.height
                # and camera_pos.y + camera_comp.height == __init.GAME_HEIGHT
            ):
                velocity.vy = 0
                sprite.y = init.GAME_HEIGHT - sprite.size[1]
            if velocity.vx == 0 and velocity.vy == 0:
                continue
            tiles = []
            self.quadtree.query_circle(
                (
                    sprite.x + velocity.vx + sprite.size[0] // 2,
                    sprite.y + velocity.vy + sprite.size[1] // 2,
                ),
                2 * sprite.size[0],
                tiles,
            )
            player_rect.x = sprite.x + velocity.vx
            player_rect.y = sprite.y + velocity.vy
            player_rect.w = sprite.size[0]
            player_rect.h = sprite.size[1]
            obstacles = set()
            grass = set()
            for tile in tiles:
                ttype = getComponentfromWorld(
                    world, tile, components.TileComponent
                ).type
                if ttype == "Obstacle":
                    obstacles.add(tile)
                elif ttype == "Grass":
                    grass.add(tile)
            faceObs = False
            print(velocity.vx, velocity.vy)
            print(sprite.area)
            print(player_rect.x, player_rect.y, player_rect.w, player_rect.h)
            for tile in obstacles:
                tile_rect.x = tile.sprite.x
                tile_rect.y = tile.sprite.y
                tile_rect.w = tile.sprite.size[0]
                tile_rect.h = tile.sprite.size[1]
                if sdl2.SDL_HasIntersection(player_rect, tile_rect):
                    print("hit", tile.sprite.area)
                    if velocity.vx > 0:
                        print(velocity.vx)
                        velocity.vx = tile.sprite.x - sprite.x - sprite.size[0] #, velocity.vx
                        # sprite.x = tile.sprite.x - sprite.size[0]
                        # velocity.vx = sprite.x - ()
                        if not velocity.vx >= 0:
                            print("\n\n========================vx >= 0 =====================\n")
                            print(tile.sprite.x, sprite.x, sprite.size[0])
                        #)
                    elif velocity.vx < 0:
                        velocity.vx =tile.sprite.x - sprite.x + sprite.size[0] #, velocity.vx
                        # sprite.x = tile.sprite.x + tile.sprite.size[0]
                        # velocity.vx = 0
                        if not velocity.vx <= 0:
                            print("\n\n========================vx <= 0 =============\n")
                            print(tile.sprite.x, sprite.x, sprite.size[0])
                        #)
                    if velocity.vy > 0:
                        velocity.vy =tile.sprite.y - sprite.y - sprite.size[1] #, velocity.vy
                        # sprite.y = tile.sprite.y - sprite.size[1]
                        # velocity.vy = 0
                        if not velocity.vy >= 0:
                            print("\n\n========================vy >= 0 ==============\n")
                            print(tile.sprite.y, sprite.y, sprite.size[1])
                        #)  
                    elif velocity.vy < 0:
                        velocity.vy = tile.sprite.y - sprite.y + sprite.size[1] #, velocity.vy
                        # sprite.y = tile.sprite.y + tile.sprite.size[1]
                        # velocity.vy = 0
                        if not velocity.vy <= 0:
                            print("\n\n========================vy <= 0 =====================\n")
                            print(tile.sprite.y, sprite.y, sprite.size[1])
                        #)
                    faceObs = True
                    # assert sprite.x % 64 == 0 or sprite.y % 64 == 0
                    break
            if faceObs:
                continue
            for tile in grass:
                tile_rect.x = tile.sprite.x
                tile_rect.y = tile.sprite.y
                tile_rect.w = tile.sprite.size[0]
                tile_rect.h = tile.sprite.size[1]
                if sdl2.SDL_HasIntersection(player_rect, tile_rect):
                    velocity.vx //= 2
                    velocity.vy //= 2
                    break

        print("Collision", sdl2.SDL_GetTicks() - start, "ms")

class BlendedSystem(sdl2.ext.Applicator):
    def __init__(self, quadtree):
        super().__init__()
        self.quadtree = quadtree
        self.componenttypes = (ext.Sprite, components.PlayerComponent)
    def process(self, world, componentsets):
        grass = set()
        grass_rect = sdl2.SDL_Rect(0, 0, 0, 0)
        player_rect = sdl2.SDL_Rect(0, 0, 0, 0)
        for (sprite, _) in componentsets:
            player_rect.x = sprite.x
            player_rect.y = sprite.y
            player_rect.w = sprite.size[0]
            player_rect.h = sprite.size[1]
            biggerTile = [] 
            self.quadtree.query_circle((sprite.x + sprite.size[0] // 2, sprite.y + sprite.size[1] // 2), sprite.size[0] * 3, biggerTile)
            biggerTile = set(biggerTile)

            for t in biggerTile:
                if getComponentfromWorld(world, t, components.TileComponent).type == "Grass":
                    grass_rect.x = t.sprite.x
                    grass_rect.y = t.sprite.y
                    grass_rect.w = t.sprite.size[0]
                    grass_rect.h = t.sprite.size[1]
                    if sdl2.SDL_HasIntersection(player_rect, grass_rect):
                        grass.add(t)
                    else: 
                        surface = t.sprite.surface
                        sdl2.SDL_SetSurfaceAlphaMod(surface, 255)
                        sdl2.SDL_SetSurfaceBlendMode(surface, sdl2.SDL_BLENDMODE_NONE)

        
        for grass_tile in grass:
            surface = grass_tile.sprite.surface
            sdl2.SDL_SetSurfaceBlendMode(surface, sdl2.SDL_BLENDMODE_BLEND)
            sdl2.SDL_SetSurfaceAlphaMod(surface, 100)
