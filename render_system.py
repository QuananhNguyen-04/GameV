import sdl2.ext as ext
from init import TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT
from utils import getEntityfromWorld, getComponentfromWorld
import sdl2
import components
import entities


class SoftwareRenderer(ext.SoftwareSpriteRenderSystem):
    def __init__(self, window, world, quad_tree):
        super(SoftwareRenderer, self).__init__(window)
        self.world = world
        self.quadtree = quad_tree
        # self.visibility_tiles = []
        self.fogEnt = None
        self.pre_level = None

    def scale_surface(self, sprite, zoom_level):
        width = int(TILE_SIZE // zoom_level)
        height = int(TILE_SIZE // zoom_level)
        print(width, height)

        # sprite_surface = sprite.surface.format.contents
        # scaled_surface = sdl2.SDL_CreateRGBSurfaceWithFormat(
        #     0, width, height, 32, sdl2.SDL_PIXELFORMAT_RGBA32
        # )
        # scaled_surface = sdl2.SDL_CreateRGBSurface(
        #     0,
        #     width,
        #     height,
        #     32,
        #     sprite_surface.Rmask,
        #     sprite_surface.Gmask,
        #     sprite_surface.Bmask,
        #     sprite_surface.Amask,
        # )
        new_surface = sdl2.SDL_CreateRGBSurface(0, width, height, 32, 0, 0, 0, 0)
        # Scale the original surface onto the new surface
        sdl2.SDL_UpperBlitScaled(sprite.surface, None, new_surface, None)
        # print(scaled_surface.w, scaled_surface.h)
        # return scaled_surface.contents
        return new_surface

    def render(self, component):
        start = sdl2.SDL_GetTicks()
        (camera,) = self.world.combined_components(
            [components.CameraComponent, components.Position]
        )
        camera_pos = camera[1]
        camera_size = camera[0]

        if self.fogEnt is None:
            self.fogEnt = getEntityfromWorld(self.world, entities.FogEntity)[0]
        fog = getComponentfromWorld(self.world, self.fogEnt, components.Fog)
        fog.reload(camera_pos.x, camera_pos.y, 300, 300)
        # newstart = sdl2.SDL_GetTicks()
        # print("Reload fog time:", sdl2.SDL_GetTicks() - start)
        rect = sdl2.SDL_Rect(0, 0, 0, 0)
        # semi_transparent = sdl2.SDL_MapRGBA(fog.pixfmt, 0, 0, 0, 128)
        transparent = sdl2.SDL_MapRGBA(fog.pixfmt, 0, 0, 0, 0)
        sprite_comp = list(
            self.world.combined_components([ext.Sprite, components.ObjComponent, components.Visibility])
        )
        player_list = []
        rendering_list = [
            # sprite
            # for (sprite, sprite_type, visibility) in sprite_comp
            # if (hasattr(sprite_type, "class_name") or visibility.visible)
            # and (-TILE_SIZE <= sprite.x - camera_pos.x <= camera_size.width + TILE_SIZE)
            # and (-TILE_SIZE <= sprite.y - camera_pos.y <= camera_size.height + TILE_SIZE)
        ]
        for (sprite, sprite_type, visibility) in sprite_comp:
            in_view = False
            if (-TILE_SIZE <= sprite.x - camera_pos.x <= camera_size.width + TILE_SIZE and -TILE_SIZE <= sprite.y - camera_pos.y <= camera_size.height + TILE_SIZE):
                in_view = True
            if hasattr(sprite_type, "class_name") and sprite_type.class_name == "Tile":
                if in_view:
                    rendering_list.append(sprite)
            elif visibility.visible:
                if in_view:
                    player_list.append(sprite)
        # rendering_list = sorted(rendering_list, key=self.m_sort_func)
        rendering_list.extend(player_list)
        tile_entities = []

        self.quadtree.query_rect(
            (
                camera_pos.x - TILE_SIZE,
                camera_pos.y - TILE_SIZE,
                SCREEN_WIDTH + 2 * TILE_SIZE,
                SCREEN_HEIGHT + 2 * TILE_SIZE,
            ),
            tile_entities,
        )

        # print("Query time:", sdl2.SDL_GetTicks() - newstart)
        # newstart = sdl2.SDL_GetTicks()
        rendering_list.append(fog)
        # scaled_list.append(fog)
        for tile in tile_entities:
            visibility = getComponentfromWorld(self.world, tile, components.Visibility)
            if not visibility.visible:
                continue
            # print(old, visibility.visible)
            if visibility.visible:
                rect.x = tile.sprite.x
                rect.y = tile.sprite.y
                rect.w = tile.sprite.size[0]
                rect.h = tile.sprite.size[1]
                sdl2.SDL_FillRect(
                    fog.surface,
                    rect,
                    transparent,
                )
                visibility.visible = False

        super(SoftwareRenderer, self).render(
            rendering_list, -camera_pos.x, -camera_pos.y
        )

        # print("Render time:", sdl2.SDL_GetTicks() - newstart)
        print("Rendered", sdl2.SDL_GetTicks() - start, "ms")
