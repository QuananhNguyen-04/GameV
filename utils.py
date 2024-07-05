def insideCircle(obj, cx, cy, radius):
    minx, miny, maxx, maxy = obj
    if (
        (cx - minx) ** 2 + (cy - miny) ** 2 > radius**2
        or (cx - maxx) ** 2 + (cy - miny) ** 2 > radius**2
        or (cx - maxx) ** 2 + (cy - maxy) ** 2 > radius**2
        or (cx - minx) ** 2 + (cy - maxy) ** 2 > radius**2
    ):
        return False
    return True


def clip_rect(x3, y3, x4, y4, area):
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


def getComponentfromWorld(world, entity, comptype):
    if hasattr(comptype, "__iter__") and not hasattr(comptype, "upper"):
        found_components = [
            world.components[c].get(entity, None)
            for c in comptype
            if c in world.components
        ]
        return tuple(found_components)
    ### copy ebs.World.combine_components() here
    if comptype in world.components:
        # Get the dictionary of entities and their components for the specified component type
        component_dict = world.components[comptype]
        # Retrieve the component instance for the specified entity ID
        return component_dict.get(entity, None)
    else:
        return None


def getEntityfromWorld(world, entityType):
    entity_list = [e for e in world.entities if isinstance(e, entityType)]
    # print(entityType, len(entity_list))
    return entity_list
