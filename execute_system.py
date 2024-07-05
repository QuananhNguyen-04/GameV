import sdl2.ext as ext
import components
# import utils


class ExecuteSystem(ext.System):
    def __init__(self):
        super().__init__()
        self.componenttypes = (components.Execute,)

    def process(self, world, componentsets):
        delete_list = []
        for (execute) in componentsets:
            if execute.killable:
                elist = world.get_entities(execute)
                delete_list.extend(elist)
        if delete_list == []:
            return
        world.delete_entities(delete_list)
