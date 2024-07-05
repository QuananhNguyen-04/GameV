import sdl2.ext as ext
import sdl2
import components
import entities
import heapq
from utils import getEntityfromWorld, getComponentfromWorld


class CommandSystem(ext.Applicator):
    class PriorityQueueItem:
        def __init__(self, item, priority):
            self.item = item
            self.priority = priority

        def __lt__(self, other):
            return self.priority < other.priority

    def __init__(self, quadtree):
        super().__init__()
        self.componenttypes = (
            components.PlayerComponent,
            ext.Sprite,
            components.Focus,
            components.Path,
        )
        self.quadtree = quadtree
        self.camera = None

    def heuristic(self, start_pos, end_pos) -> int:
        return abs(start_pos.x - end_pos.x) // start_pos.size[0] + abs(start_pos.y - end_pos.y) // start_pos.size[1]

    def astar(self, world, start, end):
        """
        Perform A* pathfinding algorithm using the given start and end points.

        Args:
            `start` (ext.Sprite): The starting sprite of the path.
            `end` (ext.Sprite): The ending sprite of the path.

        Returns:
            list: The sequence of points that form the shortest path from start to end.
        """
        start_tiles = []
        self.quadtree.retrieve((start.x + start.size[0] // 2, start.y + start.size[1] // 2, 0, 0), start_tiles)
        start = start_tiles[0].sprite
        open_set = []
        heapq.heappush(
            open_set, self.PriorityQueueItem(start, self.heuristic(start, end))
        )
        closed_set = set()
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, end)}
        while open_set:
            current = heapq.heappop(open_set).item
            # print(open_set)
            current_w, current_h = current.size
            center_x, center_y = current.x + current_w // 2, current.y + current_h // 2
            # print("Current:", current.area)
            # print("End:", end.area)
            if current.area == end.area:
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                    print("trace back")
                path.reverse()
                return path

            closed_set.add(current.area)
            neighbors = []
            self.quadtree.query_circle(
                (center_x, center_y), current_w,
                neighbors,
            )
            neighbors_dict = {
                (neighbor.sprite.x, neighbor.sprite.y): neighbor
                for neighbor in neighbors
            }
            # for neighbor in neighbors_dict:
            #     print("neighbor:", neighbor) 
            # print("====== =======\nCurrent:", current.area)
            # print("neighbors", len(neighbors))
            # print("G score:", g_score[current])
            for dx, dy in ((-1, 0), (0, -1), (1, 0), (0, 1)):
                neighbor = (
                    (current.x + dx * current_w) // current_w * current_w,
                    (current.y + dy * current_h) // current_h * current_h,
                )
                assert neighbor[0] % 64 == 0 and neighbor[1] % 64 == 0
                neighbor_entity = neighbors_dict.get(neighbor)

                if neighbor_entity is None:
                    continue

                etype = getComponentfromWorld(
                    world, neighbor_entity, components.TileComponent
                ).type
                if neighbor_entity.sprite.area in closed_set or etype == "Obstacle":
                    # if neighbor_entity.sprite.area in closed_set:
                    #     print("Blocked", neighbor_entity.sprite.area)
                    # else:
                    #     print("Obstacle", neighbor_entity.sprite.area)
                    continue

                tentative_g_score = g_score[current] + 1
                if etype == "Grass":
                    tentative_g_score += 2
                # for item in f_score:
                # print(item, type(item))
                # print(neighbor_entity.sprite.area)
                # print("Guess g score",tentative_g_score)
                # if neighbor_entity.sprite in g_score:
                #     print("Current g score",g_score[neighbor_entity.sprite])
                if (
                    neighbor_entity.sprite not in g_score
                    or tentative_g_score < g_score[neighbor_entity.sprite]
                ):
                    came_from[neighbor_entity.sprite] = current
                    g_score[neighbor_entity.sprite] = tentative_g_score
                    f_score[neighbor_entity.sprite] = (
                        tentative_g_score + self.heuristic(neighbor_entity.sprite, end)
                    )
                    assert self.heuristic(neighbor_entity.sprite, end) < 100
                    heapq.heappush(
                        open_set,
                        self.PriorityQueueItem(
                            neighbor_entity.sprite, f_score[neighbor_entity.sprite]
                        ),
                    )

    def process(self, world, componentsets):

        if self.camera is None:
            self.camera = getEntityfromWorld(world, entities.CameraEntity)[0]

        camera = getComponentfromWorld(world, self.camera, components.Position)
        start = sdl2.SDL_GetTicks()
        mouse_bstate = ext.mouse_button_state()
        if not mouse_bstate.any_pressed:
            return

        if mouse_bstate.left == 1:
            mouse_pos = ext.mouse_coords()
            mouse_pos_x = (mouse_pos[0] + camera.x) 
            mouse_pos_y = (mouse_pos[1] + camera.y) 
            print(mouse_pos, camera.x, camera.y, mouse_pos_x, mouse_pos_y)
        else:
            # if mouse_bstate.right == 1:
            return

        end_sprite = []
        if not self.quadtree.retrieve(
            (mouse_pos_x, mouse_pos_y, 0, 0), end_sprite
        ):
            print("no sprite found")
            return
        
        end_sprite = end_sprite[0]
        etype = getComponentfromWorld(world, end_sprite, components.TileComponent).type
        if etype == "Obstacle":
            # print("obstacle")
            return
        # print(end_sprite.sprite.area)

        for player, sprite, focus, comp_path in componentsets:
            if not focus.focused:
                continue
            
            # print("player:", sprite.area)
            path = self.astar(world, sprite, end_sprite.sprite)
            if path:
                print([item.area for item in path])
                comp_path.assign_path(path)
        print("CommandSystem time:",sdl2.SDL_GetTicks() - start)