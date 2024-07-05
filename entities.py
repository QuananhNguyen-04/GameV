import sdl2.ext
import components

class CameraEntity(sdl2.ext.Entity):
    def __init__(self, world, x, y, w, h) -> None:
        super().__init__()
        self.camera = components.CameraComponent(w, h)
        self.position = components.Position(x, y)
        self.velocity = components.Velocity()
        self.zoom = components.Zoom()
class TileEntity(sdl2.ext.Entity):
    def __init__(self, world, x, y, type, factory, sprite_img) -> None:
        super().__init__()
        self.tile = components.TileComponent(type)
        self.sprite = factory.from_image(sprite_img)
        if (type == "Grass"):
            self.sprite.depth = 1
        self.sprite.position = x, y
        self.visible = components.Visibility(False, True if type == "Obstacle" else False)

class PlayerEntity(sdl2.ext.Entity):
    def __init__(self, world, x, y, health, type, focus, factory, spriteLists) -> None:
        super().__init__()
        self.player = components.AllyComponent(type, factory, spriteLists)
        self.velocity = components.Velocity()
        self.sprite = factory.from_image(spriteLists["right"])
        self.sprite.position = x, y
        self.visible = components.Visibility(True)
        self.rays = components.Ray(self.sprite, 18, 200)
        self.health = components.Health(health)
        self.execute = components.Execute()
        self.focus = components.Focus(focus)
        self.path = components.Path()
        # self.range = components.Ray(self.sprite.position, 12, 100)

class EnemyEntity(sdl2.ext.Entity):
    def __init__(self, world, x, y, health, type, focus, factory, spriteLists) -> None:
        super().__init__()
        self.player = components.EnemyComponent(type, factory, spriteLists)
        self.velocity = components.Velocity()
        self.sprite = factory.from_image(spriteLists["right"])
        self.sprite.position = x, y
        self.visible = components.Visibility(False)
        self.rays = components.Ray(self.sprite, 18, 200)
        self.health = components.Health(health)
        self.execute = components.Execute()
        self.focus = components.Focus(focus)
        self.path = components.Path()
        # self.range = components.Ray(self.sprite.position, 12, 100)
class FogEntity(sdl2.ext.Entity):
    def __init__(self, world, w, h, sw, sh) -> None:
        super().__init__()
        self.surface = components.Fog(w, h, sw, sh)

class GlobalState(sdl2.ext.Entity):
    def __init__(self, world, state, value) -> None:
        super().__init__()
        self.state = components.State(state, value)