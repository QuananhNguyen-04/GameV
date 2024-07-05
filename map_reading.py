# ! using to run tilemap
import pytmx
import sdl2.ext as ext
from entities import TileEntity
import __init

RESOURCES = ext.Resources("./resources")

tile1_path = RESOURCES.get_path("dirtland1.png")
tile2_path = RESOURCES.get_path("dirtland2.png")
tile3_path = RESOURCES.get_path("grass.png")
tile4_path = RESOURCES.get_path("mount1.png")
tile5_path = RESOURCES.get_path("mount3.png")

tiles = {
    0: None,
    "dirtland1": (tile1_path, "Lane"),
    "dirtland2": (tile2_path, "Lane"),
    "grass": (tile3_path, "Grass"),
    "mount1": (tile4_path, "Obstacle"),
    "mount3": (tile5_path, "Obstacle"),
}

# Mapping tile types
tiles_type = {
    1: "Lane",
    2: "Lane",
    3: "Grass",
    4: "Obstacle",
}


def read_tiledmap(world, factory, quad, path="./resources/untitled.tmx"):
    tmx_data = pytmx.TiledMap(path)
    height = tmx_data.tileheight
    width = tmx_data.tilewidth
    __init.GAME_HEIGHT = tmx_data.height * height
    __init.GAME_WIDTH = tmx_data.width * width
    if quad.boundary != (0, 0, __init.GAME_WIDTH, __init.GAME_HEIGHT):
        quad.boundary = (0, 0, __init.GAME_WIDTH, __init.GAME_HEIGHT)
    # print(tmx_data.gidmap)
    # print(tmx_data.imagemap)
    # print(tmx_data.tiledgidmap)
    tileset_name = [t.name for t in tmx_data.tilesets]
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for obj in layer:
                # gid_key = tile_new_dict[obj[2]]
                # print(obj[2])
                tile_source = tiles[tileset_name[tmx_data.tiledgidmap[obj[2]] - 1]]
                tile_entity = TileEntity(
                    world,
                    obj[0] * width,
                    obj[1] * height,
                    tile_source[1],
                    factory,
                    tile_source[0],
                )
                if not quad.insert(tile_entity):
                    print("Failed to insert", tile_entity.sprite.area)
            break
    # assert 0