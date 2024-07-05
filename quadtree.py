class Quadtree:
    def __init__(self, boundary, capacity = 3):
        self.boundary = boundary  # (x, y, width, height)
        self.capacity = capacity
        self.tiles = []
        self.divided = False

    def subdivide(self):
        x, y, w, h = self.boundary
        # print("quad boundary", x, y, w, h)
        half_w, half_h = w // 2, h // 2
        self.northeast = Quadtree((x + half_w, y, half_w, half_h), self.capacity)
        self.northwest = Quadtree((x, y, half_w, half_h), self.capacity)
        self.southeast = Quadtree((x + half_w, y + half_h, half_w, half_h), self.capacity)
        self.southwest = Quadtree((x, y + half_h, half_w, half_h), self.capacity)
        self.divided = True

    def insert(self, tile):
        if not self.contains(tile.sprite.area):
            # print("not cotains", tile.sprite.area)
            # print(self.boundary)
            return False

        if len(self.tiles) < self.capacity:
            self.tiles.append(tile)
            return True
        else:
            if not self.divided:
                self.subdivide()

            if self.northeast.insert(tile):
                return True
            elif self.northwest.insert(tile):
                return True
            elif self.southeast.insert(tile):
                return True
            elif self.southwest.insert(tile):
                return True

    def contains(self, area):
        x, y, w, h = self.boundary
        minx, miny, maxx, maxy = area
        return (x <= (minx + maxx) // 2  <= x + w and y <= (miny + maxy) // 2 <= y + h)

    def query_circle(self, center, radius, found):
        """
        Query the Quadtree for all tiles that intersect with the given circle.

        Args:
            `center` (tuple): A tuple representing the center of the circle to query, in the format (x, y).
            `radius` (int or tuple): A single integer representing the radius of the circle or a tuple representing the inner and outer radius of the circle.
            `found` (list): A list to store the found tiles in.

        Returns:
            None
        """
        x, y, w, h = self.boundary
        cx, cy = center

        if not self.intersects_circle(cx, cy, radius):
            return

        for tile in self.tiles:
            if self.inside_circle(tile.sprite.area, cx, cy, radius):
                found.append(tile)

        if self.divided:
            self.northwest.query_circle(center, radius, found)
            self.northeast.query_circle(center, radius, found)
            self.southwest.query_circle(center, radius, found)
            self.southeast.query_circle(center, radius, found)
    def retrieve(self, rect, found):
        x, y, w, h = self.boundary
        rx, ry, rw, rh = rect
        if not ((x <= rx and rx + rw <= x + w) or (y <= ry and ry + rh <= y + h)):
            return False
        for tile in self.tiles:
            a, b, c, d = tile.sprite.area
            # print("tiles area", a, b, c, d)
            if a <= rx <= c - rw and b <= ry <= d - rh:
                found.append(tile)
                print("found", found)
                return True
        
        if self.divided:
            if self.northwest.retrieve(rect, found):
                return True
            if self.northeast.retrieve(rect, found):
                return True
            if self.southwest.retrieve(rect, found):
                return True
            if self.southeast.retrieve(rect, found):
                return True
        return False
    def query_rect(self, rect, found):
        '''
        Query the Quadtree for all tiles that intersect with the given rectangle.

        Args:
            `rect` (tuple): A tuple representing the rectangle to query, in the format
                (x, y, width, height).
            `found` (list): A list to store the found tiles in.

        Returns:
            None
        '''
        x, y, w, h = self.boundary
        rx, ry, rw, rh = rect
        # if not (x <= rx and rx + rw <= x + w and y <= ry and ry + rh <= y + h):
        #     return
        if x + w < rx or rx + rw < x or y + h < ry or ry + rh < y:
            return
        for tile in self.tiles:
            a, b, c, d = tile.sprite.area
            if rx <= a and c <= rx + rw and ry <= b and d <= ry + rh:
                found.append(tile)

        if self.divided:
            self.northwest.query_rect(rect, found)
            self.northeast.query_rect(rect, found)
            self.southwest.query_rect(rect, found)
            self.southeast.query_rect(rect, found)
    def intersects_circle(self, cx, cy, radius):
        radbig = None
        if hasattr(radius, "__iter__"):
            radbig = radius[1]
        else:
            radbig = radius
        x, y, w, h = self.boundary
        closestX = clamp(cx, x, x + w)
        closestY = clamp(cy, y, y + h)
        distanceX = cx - closestX
        distanceY = cy - closestY
        return (distanceX ** 2 + distanceY ** 2) <= (radbig ** 2)

    def inside_circle(self, obj, cx, cy, radius):
        minx, miny, maxx, maxy = obj
        if hasattr(radius, "__iter__"):
            assert len(radius) == 2
            radsmall = radius[0]
            radbig = radius[1]
            return ((cx - minx) ** 2 + (cy - miny) ** 2 >= radsmall ** 2 and \
               (cx - maxx) ** 2 + (cy - miny) ** 2 >= radsmall ** 2 and \
               (cx - maxx) ** 2 + (cy - maxy) ** 2 >= radsmall ** 2 and \
               (cx - minx) ** 2 + (cy - maxy) ** 2 >= radsmall ** 2) and \
               ((cx - minx) ** 2 + (cy - miny) ** 2 <= radbig ** 2 or \
               (cx - maxx) ** 2 + (cy - miny) ** 2 <= radbig ** 2 or \
               (cx - maxx) ** 2 + (cy - maxy) ** 2 <= radbig ** 2 or \
               (cx - minx) ** 2 + (cy - maxy) ** 2 <= radbig ** 2) 
        
        return (cx - minx) ** 2 + (cy - miny) ** 2 <= radius ** 2 or \
               (cx - maxx) ** 2 + (cy - miny) ** 2 <= radius ** 2 or \
               (cx - maxx) ** 2 + (cy - maxy) ** 2 <= radius ** 2 or \
               (cx - minx) ** 2 + (cy - maxy) ** 2 <= radius ** 2

def clamp(val, min_val, max_val):
    return max(min(val, max_val), min_val)