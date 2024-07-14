from sdl2 import ext
import sdl2
import entities
import components
import math
from utils import getEntityfromWorld, getComponentfromWorld, clip_rect
import init


class VisibleSystem(ext.Applicator):
    def __init__(self):
        super().__init__()
        # self.componenttypes = (components.AllyComponent, components.Focus)
        self.componenttypes = (components.Visibility, components.Focus, components.Team)

    def process(self, world, componentsets):
        pass
        # # for player, focus in componentsets:
        # #     if focus.focused is True:
        # #         ally_comp = world.combined_components(
        # #             [components.Visibility, components.AllyComponent]
        # #         )
        # #         for visibility, ally_player in ally_comp:
        # #             visibility.visible = True
        # #         return
        # # enemy_comp = world.combined_components(
        # #     [components.Visibility, components.EnemyComponent]
        # # )
        # # for visibility, enemy_player in enemy_comp:
        # #     visibility.visible = True
        # state = world.get_components(components.State)[0]
        # state_dict = state.stateList
        # team = state_dict["Team"]

        # for visibility, focus, pteam in componentsets:
        #     if pteam.team == team:




class RaySystem(ext.Applicator):
    def __init__(self, quad_tree):
        super().__init__()
        self.componenttypes = (
            components.Ray,
            components.Visibility,
            ext.Sprite,
        )
        self.quad_tree = quad_tree
        self.tile_list = None

    def process(self, world, componentsets):
        start = sdl2.SDL_GetTicks()
        for ray, visibility, sprite in componentsets:
            if visibility.visible is False:
                continue
            px, py = (
                sprite.position[0] + sprite.size[0] // 2,
                sprite.position[1] + sprite.size[1] // 2,
            )
            radius = ray.radius
            ray.pos = (px, py)
            if ray.end_points is None:
                ray.end_points = []
                for angle in range(0, 360, ray.n):
                    rad_angle = math.radians(angle)
                    dx = int(radius * math.cos(rad_angle))
                    dy = int(radius * math.sin(rad_angle))
                    x_end = px + dx
                    y_end = py + dy
                    ray.end_points.append((rad_angle, x_end, y_end, dx, dy))
            # ray.end_points.clear()
            # local_tiles = set(
            #     [
            #         e.sprite
            #         for e in self.tile_list
            #         if (insideCircle(e.sprite.area, px, py, ray.radius)) is True
            #     ]
            # )
            local_tiles = []
            self.quad_tree.query_circle((px, py), ray.radius, local_tiles)
            obstacle_lists = set()
            for tile_entity in local_tiles:
                if (
                    getComponentfromWorld(
                        world, tile_entity, components.ObjComponent
                    ).type
                    != "Obstacle"
                ):
                    continue
                obstacle_lists.add(tile_entity.sprite)
            # print(len(local_tiles))
            for i, ele in enumerate(ray.end_points):
                rad_angle = ele[0]
                dx = ele[3]
                dy = ele[4]
                x_end = px + dx
                y_end = py + dy
                for tiles in obstacle_lists:
                    if clip_rect(px, py, x_end, y_end, tiles.area) is True:
                        x_end = tiles.area[0] + tiles.size[0] // 2
                        y_end = tiles.area[1] + tiles.size[1] // 2
                ray.end_points[i] = (rad_angle, x_end, y_end, dx, dy)
        print("Rays", sdl2.SDL_GetTicks() - start, "ms")


class FoWSystem(ext.Applicator):
    def __init__(self, quadtree):
        super().__init__()
        self.componenttypes = (components.Ray, components.Visibility, components.Team)
        self.camera = None
        self.quadtree = quadtree

    def clip_rect(self, x3, y3, x4, y4, area):
        def is_outside(x1, y1, area):
            INSIDE = 0000
            LEFT = 1
            RIGHT = 2
            BOTTOM = 4
            TOP = 8

            in1 = INSIDE
            if x1 < area[0]:
                in1 |= LEFT
            elif x1 > area[2]:
                in1 |= RIGHT
            if y1 < area[1]:
                in1 |= TOP
            elif y1 > area[3]:
                in1 |= BOTTOM
            return in1

        x1 = area[0]
        y1 = area[1]
        x2 = area[2]
        y2 = area[3]
        # print(x3, y3, x4, y4, area)
        outcode1 = is_outside(x3, y3, area)
        outcode2 = is_outside(x4, y4, area)
        if outcode1 & outcode2:
            return False
        if not (outcode1 | outcode2):
            return True

        left = False
        right = False

        for x, y in [(x1, y1), (x1, y2), (x2, y1), (x2, y2)]:
            function = (x - x3) * (y4 - y3) - (y - y3) * (x4 - x3)
            if function == 0:
                return True
            if function < 0:
                left = True
            else:
                right = True
        if left and right:
            return True
        return False

    def process(self, world, componentsets):
        # start = sdl2.SDL_GetTicks()
        # if self.tile_list is None:
        #     self.tile_list = set(getEntityfromWorld(world, entities.TileEntity))
        if self.camera is None:
            self.camera = getEntityfromWorld(world, entities.CameraEntity)[0]
        camera_pos = getComponentfromWorld(world, self.camera, components.Position)
        state = list(world.get_components(components.State))[0]
        state_dict = state.stateList
        team = state_dict["Team"]
        for ray, p_visibility, p_team in componentsets:
            if p_team.team != team:
                continue
            if p_visibility.visible is False:
                continue
            px, py = ray.pos
            if (px < -ray.radius + camera_pos.x) or (
                px > init.SCREEN_WIDTH + ray.radius + camera_pos.x
            ):
                continue
            if (py < -ray.radius + camera_pos.y) or (
                py > init.SCREEN_HEIGHT + ray.radius + camera_pos.y
            ):
                continue
            local_tile_list = []
            self.quadtree.query_circle((px, py), ray.radius, local_tile_list)
            tile_comp_list = set(
                [
                    getComponentfromWorld(
                        world, tile, [ext.Sprite, components.Visibility]
                    )
                    for tile in local_tile_list
                ]
            )
            e_list = world.combined_components(
                [ext.Sprite, components.Visibility, components.PlayerComponent]
            )
            for sprite, visibility, enemy in e_list:
                tile_comp_list.add((sprite, visibility))

            for tile, visibility in tile_comp_list:
                if visibility.visible is True:
                    continue
                if (
                    not -init.TILE_SIZE
                    <= tile.position[0] - camera_pos.x
                    <= init.SCREEN_WIDTH + init.TILE_SIZE
                    or not -init.TILE_SIZE
                    <= tile.position[1] - camera_pos.y
                    <= init.SCREEN_HEIGHT + init.TILE_SIZE
                ):
                    continue

                for ray_line in ray.end_points:
                    if (
                        self.clip_rect(ray.pos[0], ray.pos[1], ray_line[1], ray_line[2], tile.area) is True
                    ):
                        visibility.visible = True
                        break

        # print("FOW", sdl2.SDL_GetTicks() - start, "ms")
