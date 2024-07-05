import random
import sdl2.ext as ext
import sdl2
from quadtree import Quadtree
from __init import (
    GAME_HEIGHT,
    GAME_WIDTH,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    TILE_SIZE,
    FRAME_TIME
)
import __init
from map_reading import read_tiledmap
from system import (
    InputSystem,
    MovementSystem,
    CameraSystem,
    CollisionSystem,
    BlendedSystem,
)
from command_system import CommandSystem
from render_system import SoftwareRenderer
from status_system import StatusSystem
from fog_system import FoWSystem, RaySystem, VisibleSystem
from kill_system import KillSystem
from entities import CameraEntity, PlayerEntity, FogEntity, GlobalState, EnemyEntity
# from zoom_system import ZoomSystem
from toggle_vision_system import ToggleVisionSystem
from execute_system import ExecuteSystem

RESOURCES = ext.Resources("./resources")
pRight_path = RESOURCES.get_path("spearman-4-r.png")
pLeft_path = RESOURCES.get_path("spearman-4-l.png")
eRight_path = RESOURCES.get_path("enspearman-4-r.png")
eLeft_path = RESOURCES.get_path("enspearman-4-l.png")
# pUp_path = RESOURCES.get_path("pUp.png")
# pDown_path = RESOURCES.get_path("pDown.png")
# tile0_path = RESOURCES.get_path("dirtland2.png")
# tile1_path = RESOURCES.get_path("dirtland1.png")
# tile2_path = RESOURCES.get_path("grass.png")
# tile3_path = RESOURCES.get_path("mount1.png")
# tile4_path = RESOURCES.get_path("mount2.png")
# # tile5_path = RESOURCES.get_path("t5.png")
# # tile6_path = RESOURCES.get_path("t6.png")
# # tile7_path = RESOURCES.get_path("t7.png")
# tiles = [
#     tile0_path,
#     tile1_path,
#     tile2_path,
#     tile3_path,
#     tile4_path,
# ]

pImages = {
    "left": pLeft_path,  # Left direction
    "right": pRight_path,  # Right direction
    # "up": pUp_path,  # Up direction
    # "down": pDown_path,  # Down direction
}
eImages = {
    "left": eLeft_path,  # Left direction
    "right": eRight_path,  # Right direction
}
# tiles_type = {
#     0: "Lane",
#     1: "Lane",
#     2: "Grass",
#     3: "Obstacle",
#     4: "Obstacle",
# }
# MAP = [
#     [
#         random.choices([0, 1, 2, 3, 4], weights=[0.4, 0.2, 0.1, 0.2, 0.1])[0]
#         for _ in range(GAME_WIDTH // TILE_SIZE)
#     ]
#     for _ in range(GAME_HEIGHT // TILE_SIZE)
# ]


def inframe(x) -> int:
    return x // __init.TILE_SIZE * __init.TILE_SIZE


def run():
    sdl2.ext.init()
    factory = ext.SpriteFactory(sdl2.ext.SOFTWARE)

    window = sdl2.ext.Window(
        "PySDL2 Game", size=(__init.SCREEN_WIDTH, __init.SCREEN_HEIGHT)
    )
    window.show()

    world = sdl2.ext.World()

    # Create the camera entity

    # MAP_TILES = []
    start = sdl2.SDL_GetTicks()
    quad = Quadtree((0, 0, __init.GAME_WIDTH, __init.GAME_HEIGHT), 15)

    read_tiledmap(world, factory, quad, "./resources/map1.tmx")

    print(f"Quadtree time: {sdl2.SDL_GetTicks() - start} ms")
    # Create player entities
    PlayerEntity(
        world, 2 * TILE_SIZE, 2 * TILE_SIZE, 100, "player1", True, factory, pImages
    )
    PlayerEntity(
        world,
        24 * TILE_SIZE,
        7 * TILE_SIZE,
        random.randint(5, 100),
        "player2",
        False,
        factory,
        pImages,
    )
    EnemyEntity(
        world,
        37 * TILE_SIZE,
        17 * TILE_SIZE,
        random.randint(5, 100),
        "enemy",
        False,
        factory,
        eImages,
    )

    # PlayerEntity(
    #     world,
    #     random.randint(0, 30) * TILE_SIZE,
    #     random.randint(0, 30) * TILE_SIZE,
    #     random.randint(5, 100),
    #     "player3",
    #     factory,
    #     pImages,
    # )

    CameraEntity(world, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    FogEntity(world, GAME_WIDTH, GAME_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT)
    GlobalState(world, ["Focus", "Player"], [True, 0])
    # Create and add systems to the world
    renderer = SoftwareRenderer(window, world, quad)
    camera_system = CameraSystem()
    raycast_system = RaySystem(quad)
    movement_system = MovementSystem()
    collision_system = CollisionSystem(quad)
    kill_system = KillSystem()
    fow_system = FoWSystem(quad)
    status_system = StatusSystem()
    input_system = InputSystem()
    # zoom_system = ZoomSystem()

    # world.add_system(zoom_system)
    world.add_system(camera_system)
    world.add_system(ToggleVisionSystem())
    world.add_system(VisibleSystem())
    world.add_system(raycast_system)
    world.add_system(fow_system)
    world.add_system(CommandSystem(quad))
    world.add_system(input_system)
    world.add_system(status_system)
    world.add_system(collision_system)
    world.add_system(kill_system)
    world.add_system(ExecuteSystem())
    world.add_system(movement_system)
    world.add_system(BlendedSystem(quad))
    world.add_system(renderer)

    running = True
    min_fps = 1000
    while running:
        for event in sdl2.ext.get_events():
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            if event.type == sdl2.SDL_KEYDOWN:
                key = event.key.keysym.sym
                if key == sdl2.SDLK_ESCAPE:
                    running = False
                    break
                elif key == sdl2.SDLK_l:
                    pausing = True
                    while pausing:
                        event = sdl2.SDL_Event()
                        sdl2.SDL_WaitEvent(event)
                        if event.type == sdl2.SDL_QUIT:
                            running = False
                            pausing = False
                            break
                        if event.type == sdl2.SDL_KEYDOWN:
                            key = event.key.keysym.sym
                            if key == sdl2.SDLK_l:
                                pausing = False
                                break

        # Render system processes entities
        frame_start = sdl2.SDL_GetTicks()

        # Update systems
        world.process()

        # Render system processes entities
        frame_end = sdl2.SDL_GetTicks()
        frame_duration = frame_end - frame_start
        real_fps = 1000 / frame_duration

        print(f"FPS: {'{:0.2f}'.format(real_fps)}")
        print(f"frame duration: {frame_duration}")
        min_fps = min(real_fps, min_fps)
        # if min_fps < 15:
        #     break
        # if frame_duration < FRAME_TIME:
        #     sdl2.SDL_Delay(FRAME_TIME - frame_duration)
    print (f"Min FPS: {'{:0.2f}'.format(min_fps)}")
    sdl2.ext.quit()


if __name__ == "__main__":
    run()
